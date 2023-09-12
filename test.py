import bot_reply
import cstatus
import asyncio
import os
import json

# print(os.getcwd())

async def q():
    csi1 = json.dumps({
        "routine": "standard",
        "superstate": "úvod",
       "user_reply": "a co ty jak se máš",
        "last_states": ["state_intro"],
        "states_usage": {},
        "turns_since_initiative": 0})

    cso1 = await bot_reply.reply(csi1)
    cso1.show()


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
