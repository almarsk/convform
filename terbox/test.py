from terbox.bot_reply import reply

import asyncio
import os
import json

async def print_cstatus(csi, user_id):
    csi1 = json.dumps(
        csi
    )
    cso1 = await reply(csi1, user_id, "vtipobot")


def dbg_test(csi, user_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_cstatus(csi, user_id))

if __name__ == "__main__":
    dbg_test({'reply': 'Těší mě, že se poznáváme.',
     'user_reply': 'mně také. řekni vtip',
     'last_states': ['těší mě'],
     'states_usage': {'žádost o představení': 2, 'state_intro': 1, 'těší mě': 1},
     'turns_since_initiative': 1,
     'bot_turns': 3,
     'coda': False,
     'initiativity': 1,
     'context': {}}, 0)
