from terbox.bot_reply import reply


import asyncio
import os
import json


async def q(csi, user_id):
    csi1 = json.dumps(
        csi
    )
    cso1 = await reply(csi1, user_id, "vtipobot")


def dbg_test(csi, user_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(q(csi, user_id))

if __name__ == "__main__":
    dbg_test({
        "bot_reply": "Dobrý den",
        "user_reply": "ahoj, jak se máš?",
        "last_states": ["state_intro"],
        "states_usage":
            {"state_intro": 1,
            },
        "turns_since_initiative": 0,
        "bot_turns": 1,
        "coda": False,
        "initiativity": 0,
        "context": {}}, 0)


"""
'"{"reply": "Jak se jmenujete?", "meta": {"last_states": ["žádost o '
 'představení"], "states_usage": {"žádost o představení": 1, "state_intro": '
 '1}, "turns_since_initiative": 1, "bot_turns": 2, "coda": false, '
 '"initiativity": 0}}"'
 """
