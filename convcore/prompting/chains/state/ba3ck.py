from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

import time

how_far = 6

def ba3ck(args, bench=False):

    used_context = []
    if "context" in args:
        context_len = len(args["context"])
        if args["context"] and context_len > how_far:
            args["log"]([f"going back"])
            used_context = args["context"][0:-how_far]

    args["context"] = used_context

    return basic(args, bench=bench)
