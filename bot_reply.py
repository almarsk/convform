import cstatus
import convform

"""
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, ConversationChain, OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.buffer_window import ConversationBufferWindowMemory
"""


async def reply(cStatus) -> convform.CStatusOut:
    # set default csi, make it roll
    # in app.py get the latest user_reply and cState
    # passed via cState -> routine, superstate, last_states, states_usage, turns_since_initiative
    # passed via user_reply -> user_reply
    # if none arrives
    # -> routine = none (take the first one on rust side)
    # -> superstate = none (take the first one on rust side)
    # -> last_states = []
    # -> states_usage = {}
    # turns_since_initiative = 0


    bot_path = "convform_/bots"
    bot_name = "bohumil"
    """    csi_name = "csi0"

    csi_path = f"./convform_/bots/csi/{csi_name}.json"
    csi = cstatus.parse_json_file(csi_path)
    """
    print(vars(cStatus))
    cso = convform.CStatusOut(bot_path, bot_name, cStatus)

    return cso

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
    #
    # have AI manage            1) fallbacks 2) initiative based on flow (later establishing topics, vec dbs)
    #                           fallback-   look for intent based on names of intents
    #                                   -   create an answer trying to steer the person back
    #                                       to general overview of convo defined in state_start (TODO)
    #                           conversation with AI employed produces suggestions of new chunks of convDesign JSON
    #
