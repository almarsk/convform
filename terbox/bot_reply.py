import terbox.cstatus as cstatus
from convform import CStatusOut
from terbox.lch import fill_in
from terbox.smart_sub import check_for_prompts

import os

async def reply(cStatus, user_id, flow):
    path = "convform/bots/"

    cso = CStatusOut(flow, cStatus, path)

    filled_in_reply = cso.bot_reply
    persona = cso.persona(path, flow)

    if "###" in cso.bot_reply:
        filled_in_reply = await check_for_prompts(persona, cso.bot_reply, user_id)

    if cso.prompt is not None:
        print("todo global prompting")

        global_prompt = "zkontroluj a pokud je to nezbytně nuntné uprav poslední odpověď bota. jinak vrať stejnou odpověď.\nco by teď bot řekl:"

        filled_in_reply = await fill_in(cso.prompt, global_prompt, user_id)
        # make a function which will call gpt globally
        # make a function which will add states using 613

    cso.bot_reply = filled_in_reply
    #print(cStatus)
    cso.show()

    # prompt the intentional prompts
    #
    # if a signal is given (figure out propagating a flag through the custom structs and turning it on at the right place)
    # create a return annotation function and a compose response based on gpt check
    #
    # if empty - create a function to assemble the prompt -> context + overall intent of bot


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
