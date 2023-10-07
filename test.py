import bot_reply
import cstatus
import asyncio
import os
import json


async def q(csi):

    csi1 = json.dumps(
        csi
    )


    cso1 = await bot_reply.reply(csi1, 0, "vtipobot")


def main(csi):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(q(csi))
