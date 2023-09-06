import bot_reply
import cstatus
import asyncio
import os
import json

# print(os.getcwd())

async def q():
    csi = json.dumps({
        "routine": "standard",
        "superstate": "úvod",
        "user_reply": "ahoj",
        "last_states": ["state_intro"],
        "states_usage": {"state_intro":1},
        "turns_since_initiative": 1,
    })
    csi = json.dumps({
        "routine": "standard",
        "superstate": "úvod",
        "user_reply": "tak jo",
        "last_states": ["otázka jestli vtip"],
        "states_usage": {
            "state_intro": 1,
            "otázka jestli vtip": 1
        },
        "turns_since_initiative": 0,
    })
    cso = await bot_reply.reply(csi)
    cso.show()

loop = asyncio.get_event_loop()
loop.run_until_complete(q())
