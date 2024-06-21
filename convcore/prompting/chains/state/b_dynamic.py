import sys
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.an2fora import an2fora

import time

def b_dynamic(args, bench=False):
    args["log"](["b_dynamic"])

    # goes back to first checkpoint if there is one
    # -1 because checkpoints are taken from bot_turns which are 1 indexed
    checkpoint = (args["checkpoints"][0] - 1
        if "checkpoints" in args and args["checkpoints"]
        else len(args["context"])
        if "context" in args
        else 0)

    args["log"]([f"checkpoint {checkpoint}"])

    used_context = args["context"] if "context" in args else []
    if "context" in args:
        context_len = len(args["context"])
        if args["context"] and context_len > checkpoint:
            args["log"]([f"b-dynamic succesful - going back"])
            used_context = args["context"][0:checkpoint-1]

    args["context"] = used_context
    try:
        args["about_what"] = args["entities_all"][checkpoint][-1]
    except:
        pass

    return an2fora(args, bench=bench)
