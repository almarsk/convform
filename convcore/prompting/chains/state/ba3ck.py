from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

import time

def ba3ck(args, bench=False):
    how_far = len(args["context"]) - 3 if "context" in args else 0

    if "prompt" in args:
        split = args["prompt"].split("|")
        if len(split) > 1:
            [text, distance] = split
            how_far = int(distance)
            args["prompt"] = text

    used_context = []
    if "context" in args:
        context_len = len(args["context"])
        if args["context"] and context_len > how_far:
            args["log"]([f"going back"])
            used_context = args["context"][0:-how_far]


    args["context"] = used_context

    return basic(args, bench=bench)
