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

    print(args["checkpoints"])

    checkpoint = (args["checkpoints"][0]
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
            used_context = args["context"][0:checkpoint]

    args["context"] = used_context
    args["about_what"] = args["entities_all"][checkpoint]

    return an2fora(args, bench=bench)
