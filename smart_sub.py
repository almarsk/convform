import re
import lch
import asyncio

async def check_for_prompts(persona, reply):
    pattern = r'###(.*?)###'
    m = await asyncio.to_thread(lambda: re.sub(pattern, lambda x: asyncio.run(modify_match(persona, x)), reply))
    return m


async def modify_match(persona, match):
    captured_text = match.group(1)
    n = await lch.fill_in(persona, captured_text)
    return n
