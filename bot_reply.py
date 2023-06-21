from asyncio.tasks import sleep
from flask_sqlalchemy import query

from langchain.memory.buffer_window import ConversationBufferWindowMemory
from utils import *
import fire
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, ConversationChain, OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory



async def reply(user_reply, cState) -> str:
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
        return await state_answer(flow, cState, user_reply)

    # LangChain                 setup template work for different situations
    #                                   for when there isnt an answer
    #                                       initiative function, for other cases too - base on general description of flow
    #                                   for when bot is suggesting something and is waiting for approval
    #                                   for when bot was allowed to do it
    #                           LangChain router - multipromt chain - should take from the json based on superstate
    #                                       anotator function - dialogue act, entities
    #                                           to choose intents and states
    #
    #                                   perhaps there will be reasoning chains necesarry for understanding
    #                                   where we are in each process
    # Dumb design TODO
    #                                        redo the json format + implementation implication
    #
    #_______________________________________________________________
    # reactivity            -   in case of only overiterating steering the convo    - smart reply
    #                       -   what does it mean to steer convo?                   - general flow description + states
    #
    # steering the convo    -   next possible state in case theres not iniciative to react to
    #                       -   have AI determine whether there is no iniciative to react to
    #                               - if there is no iniciative - easy going phrase/steering the convo
    #                       -   or whether there is an uncaught intent - automate suggesting edits to the flow JSON
    #
    #
    # have AI manage            1) fallbacks 2) initiative based on flow (later establishing topics, vec dbs)
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
