from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.anafora import anafora

import time

def b_dynamic(args, bench=False):
    args["log"](["b_dynamic"])

    # goes back to first checkpoint if there is one

    checkpoint = (args["checkpoint"]
        if "checkpoint" in args
        else len(args["context"])
        if "context" in args
        else 0)

    args["log"]([f"checkpoint {checkpoint}"])

    used_context = args["context"] if "context" in args else []
    if "context" in args:
        context_len = len(args["context"])
        if args["context"] and context_len > checkpoint:
            args["log"]([f"going back"])
            used_context = args["context"][0:checkpoint]

    args["context"] = used_context

    return anafora(args, bench=bench)
