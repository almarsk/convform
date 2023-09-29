import bot_reply
import cstatus
import asyncio
import os
import json


csi1 = json.dumps({
    "user_reply": "tak jo",
    "routine": "standard",
    "superstate": "nabídka další vtip",
    "last_states": ["další vtip"],
    "states_usage": {
        "state_intro": 1,
        "těší mě": 1,
        "žádost o představení": 2,
        "pointa vtipu": 1,
        "jak se máš": 1,
        "to mě těší": 1,
        "otázka jestli vtip": 1,
        "mám se dobře": 1,
        "další vtip": 1,
        "otázka vtipu":1
    },
    "turns_since_initiative": 0
})



async def q():

    csi2 = json.dumps(
        {
            "user_reply": "tak jo, řekni",
            "routine": "standard",
            "superstate": "otázka jestli vtip",
            "last_states": ["otázka jestli vtip"],
            "states_usage": {
                "a co vy": 1,
                "žádost o představení": 2,
                "jak se máš": 1,
                "mám se dobře": 1,
                "state_intro": 1,
                "otázka jestli vtip": 1,
                "těší mě": 1,
                "to mě těší": 1},
            "turns_since_initiative": 0
        })



    cso1 = await bot_reply.reply(csi1, 0, "vtipobot")


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
