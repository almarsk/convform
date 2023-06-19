from asyncio.tasks import sleep
from flask_sqlalchemy import query

from langchain.memory.buffer_window import ConversationBufferWindowMemory
from utils import *
import fire
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, ConversationChain, OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory



async def reply2(user_reply, cState) -> str:
    await sleep(1.5)

    cState.setdefault("state", "state_start")
    cState.setdefault("global_turn", 0)
    cState.setdefault("intent_iterations", {})
    flow: dict = get_flow_json(cState["flow"])

    if cState["global_turn"] == 0:
        cState["global_turn"] += 1
        cState["state"] = "state_intro"
        init_greeting: str = flow["state_start"]["greet"]
        return init_greeting
    else:
        return state_answer(flow, cState, user_reply)

async def reply(user_reply, cState) -> str:

    template ="""Jsi hodný česky mluvící robot, který rád říká vtipy.
Mluvíš v krátkých větách.
Vždy se nejdřív zeptáš, jestli můžeš říct vtip
a až když ti to člověk dovolí řekneš ho.
{history}
{input}
AI:"""

    prompt = PromptTemplate(
        input_variables=['history', 'input'],
        partial_variables={},
        template=template
    )

    memory = ConversationBufferWindowMemory(
        memory_key='history', human_prefix="Kamarád", k=5)
    fillUpMem(cState, memory)
    llm = ChatOpenAI(openai_api_key=apiKey(), model_name= "gpt-3.5-turbo", temperature=0)
    conversation = LLMChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    response = await conversation.arun(f"Kamarád: {user_reply}" if user_reply else " ")
    print(response)
    return response


    # TODO
    #                           order of composed answer based on priority
    #                           compose answer based on matched intents, priority and over-iteration
    #                           edge-cases: all over-iterated   - over-iterated answer + steering the conversation
    #                                        no matches          - AI fallback management
    #                           come up with another state to be able to test steering the convo as a fallback
    #                           make sure the robot speech is loaded async, right now theres a hardcoded timeout
    #
    #______________________________________________________________________________________________________________
    # reactivity            -   in case of only overiterating steering the convo
    #                       -   what does it mean to steer convo?
    #                       -   each intent has possible follow-up
    #
    # steering the convo    -   next possible state in case theres not iniciative to react to
    #                       -   have AI determine whether there is no iniciative to react to
    #                               - if there is no iniciative - easy going phrase/steering the convo
    #                       -   or whether there is an uncaught intent - automate suggesting edits to the flow JSON
    #
    # over-iteration behavior - next state? steering the convo?
    #
    # have AI manage            1) fallbacks 2) establishing topics (later, vec dbs)
    #                           fallback-   look for intent based on names of intents
    #                                   -   create an answer trying to steer the person back
    #                                       to general overview of convo defined in state_start (TODO)
    #                           conversation with AI employed produces suggestions of new chunks of convDesign JSON
    #


# TESTING SECTION

async def test():
    cState0 = {
        "flow" : "zvědavobot",
    }
    cState1 = {
        "flow" : "zvědavobot",
        'global_turn': 2,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 0,
            'jak se máš': 0
        }
    }
    cState2 = {
        "flow" : "zvědavobot",
        'global_turn': 3,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 1,
            'jak se máš': 0
        }
    }
    cState3 = {
        "flow" : "zvědavobot",
        'global_turn': 3,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 2,
            'jak se máš': 1
        }
    }

    print("bot: "+await reply("", cState0))
    print("usr: "+"ahoj")
    print("bot: "+await reply("ahoj", cState1))
    print("bot: "+await reply("ahoj jak se máš", cState2))
    print("bot: "+await reply("ahoj jak se máš", cState3))


if __name__ == '__main__':
  fire.Fire(test)
