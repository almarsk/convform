import bot_reply
import cstatus
import asyncio
import os
import json


async def q():

    csi1 = json.dumps(
        {"user_reply": "tak jo",
        "reply": "chcete slyšet vtip?", "routine": "loop",
         "superstate": "otázka jestli vtip", "last_states": ["otázka jestli vtip"],
         "states_usage": {
           "žádost o představení": 1,
           "state_intro": 1,
           "jak se máš": 1,
           "otázka jestli vtip": 1
         },
         "turns_since_initiative": 0}
    )

    csi2 = json.dumps(
        {"user_reply": "tak ne",
        "reply": "chcete slyšet vtip?", "routine": "loop",
            "superstate": "otázka jestli vtip", "last_states": ["otázka jestli vtip"],
            "states_usage": {
            "žádost o představení": 1,
            "state_intro": 1,
            "jak se máš": 1,
            "otázka jestli vtip": 1
            },
            "turns_since_initiative": 0}
    )

    csi3 = json.dumps(
        {"user_reply": "tak ne jo",
        "reply": "chcete slyšet vtip?", "routine": "loop",
        "superstate": "otázka jestli vtip", "last_states": ["otázka jestli vtip"],
        "states_usage": {
        "žádost o představení": 1,
        "state_intro": 1,
        "jak se máš": 1,
        "otázka jestli vtip": 1
        },
        "turns_since_initiative": 0}
    )



    #cso1 = await bot_reply.reply(csi1, 0, "vtipobot")
    cso2 = await bot_reply.reply(csi2, 0, "vtipobot")
    cso3 = await bot_reply.reply(csi3, 0, "vtipobot")


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
