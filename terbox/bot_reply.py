from terbox import cstatus
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

    cso.bot_reply = filled_in_reply
    #print(cStatus)
    cso.show()
    return cso

# make a function which will call gpt globally
# make a function which will add states using 613
