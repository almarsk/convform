import bot_reply
import cstatus
import asyncio
import os
import json


async def q():

    csi1 = json.dumps(

        {"user_reply": "tak jo ne",
        "reply": "To rád slyším. Chcete slyšet vtip?",
        "routine": "standard",
                "superstate": "úvod",
                "last_states": ["to jsem rád","otázka jestli vtip"],
         "states_usage": {
             "state_intro": 1,
             "žádost o představení": 1,
             "jak se máš": 1,
             "těší mě": 1,
             "to jsem rád": 1,
             "otázka jestli vtip": 1,
         }, "turns_since_initiative": 0}


    )



    cso1 = await bot_reply.reply(csi1, 0, "vtipobot")


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
