from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.anafora import anafora

import time

def b_dynamic(args, bench=False):
    args["log"](["b_dynamic"])

    # goes back to first checkpoint if there is one

    checkpoint = args["checkpoint"] if "checkpoint" in args else 0
    how_far = len(args["context"]) - checkpoint if "context" in args else 0

    args["log"]([f"checkpoint {checkpoint}, how far {how_far}"])

    used_context = []
    if "context" in args:
        context_len = len(args["context"])
        if args["context"] and context_len > how_far:
            args["log"]([f"going back"])
            used_context = args["context"][0:-how_far]


    args["context"] = used_context

    return anafora(args, bench=bench)
