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
Zaznamenej u jednotlivých popisů,\
jestli a kde začíná odpovídající segment v aktuální replice.\
Hodnoť jen poslední repliku, \
ty předchozí jsou zde jen pro kontext''',
        'parameters': {
            'type': 'object',
            'properties': {
                f"{intent}": {
                    "type": "integer",
                    "description": f'''\
číslo písmene od začátku aktuální repliky, kde začíná část repliky,\
ve které uživatel {prompt}, nebo -1 pokud popis neodpovídá''',
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
