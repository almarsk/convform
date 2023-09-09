import bot_reply
import cstatus
import asyncio
import os
import json

# print(os.getcwd())

async def q():
    csi1 = json.dumps({
        "routine": "standard",
        "superstate": "otázka jestli vtip",
       "user_reply": "já řeknu",
        "last_states": ["otázka jestli vtip"],
        "states_usage": {"žádost o představení": 1, "state_intro": 1, "otázka jestli vtip": 1},
        "turns_since_initiative": 0})

    cso1 = await bot_reply.reply(csi1)
    cso1.show()


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
