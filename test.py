import bot_reply
import cstatus
import asyncio
import os
import json

# print(os.getcwd())

async def q():
    csi1 = json.dumps({
        "user_reply": "ahoj",
        "routine": "standard",
        "superstate": "úvod",
        "last_states": ["state_intro"],
        "states_usage": {"state_intro": 1},
        "turns_since_initiative": 0
    })

    cso1 = await bot_reply.reply(csi1)
    cso1.show()


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
