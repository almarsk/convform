import bot_reply
import cstatus
import cstatus
import asyncio
import os

# print(os.getcwd())

async def q():
    csi = cstatus.CStatusIn(
        "",
        "",
        "čauky",
        [],
        {},
        2
    )
    cso = await bot_reply.reply(csi)
    cso.show()


loop = asyncio.get_event_loop()
loop.run_until_complete(q())
