import bot_reply
import cstatus
import asyncio
import os
import json

async def q():

    csi1 = json.dumps(
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



    cso1 = await bot_reply.reply(csi1)


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
