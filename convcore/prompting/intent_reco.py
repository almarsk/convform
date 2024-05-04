from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from .utilz import api_key

import json
import pprint

def intent_reco(prompts, convo, log):
    api_key()

    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)

    messages: list[HumanMessage | AIMessage | SystemMessage] = [
        HumanMessage(content=turn["say"])
        if turn["who"] == "human"
        else AIMessage(content=turn["say"])
        for turn in convo
    ]

    messages.insert(-1, SystemMessage(content="\nAktuální replika:"))

    functions=[{
        'name': 'zadej_zacatek_odpovidajiciho_segmentu',
        'description': '''\
Funkce popisuje, jestli uživatel udělal nebo neudělal ve své replice to, co se píše v popisce. \
-1 pokud to neudělal a 1 pokud ano. \
Hodnoť jen poslední repliku, \
ty předchozí jsou zde jen pro kontext''',
        'parameters': {
            'type': 'object',
            'properties': {
                f"{intent}": {
                    "type": "integer",
                    "description": f'''\
pokud uživatel {prompt} tak vrať 1. -1 pokud ne. Buď velmi přísný.''',
                } for intent, prompt in prompts.items()
            },
        'required': [f"{intent}" for intent, _ in prompts.items()]
    }}]

    result = chat.invoke(messages, functions=functions)
    result = result.additional_kwargs

    addition = [[str(message) for message in messages], functions, result]
    log(addition)

    if "function_call" in result:
        decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))

        return decoded_arguments
    else:
        return {}
