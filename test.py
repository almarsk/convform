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
        "user_reply": "ahoj",
        "last_states": ["state_intro"],
        "states_usage": {"state_intro":1},
        "turns_since_initiative": 1,
    })

    csi2 = json.dumps({
        "routine": "standard",
            "superstate": "úvod",
            "user_reply": "jak se máš?",
            "last_states": [
                "žádost o představení",
            ],
            "states_usage": {
                "žádost o představení": 1,
                "state_intro": 1,
            },
            "turns_since_initiative": 0,
    })

   # cso1 = await bot_reply.reply(csi1)
   # cso1.show()

    cso2 = await bot_reply.reply(csi2)
    cso2.show()

loop = asyncio.get_event_loop()
loop.run_until_complete(q())
