import re
import lch
import asyncio

async def check_for_prompts(persona, reply, user_id):
    pattern = r'###(.*?)###'
    m = await asyncio.to_thread(lambda: re.sub(pattern, lambda x: asyncio.run(modify_match(persona, x, user_id)), reply))

    return re.sub("\n", "<br>", m)


async def modify_match(persona, match, user_id):
    captured_text = match.group(1)
    n = await lch.fill_in(persona, captured_text, user_id)
    return n
