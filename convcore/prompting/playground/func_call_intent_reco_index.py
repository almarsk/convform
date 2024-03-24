from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from ..utilz import api_key

import json
import pprint

def intent_reco(prompts, convo):
    api_key()

    gpt4 = "gpt-4-0125-preview"
    gpt3 = "gpt-3.5-turbo-0613"

    chat = ChatOpenAI(model=gpt3, temperature=0)

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
index znaku aktuální repliky, kde začíná segment,\
kde uživatel {prompt}, nebo -1 pokud popis neodpovídá''',
                } for intent, prompt in enumerate(prompts, start=1)
            },
        'required': [f"{intent}" for intent, _ in enumerate(prompts, start=1)]
    }}]

    result = chat.invoke(messages, functions=functions)
    result = result.additional_kwargs

    pprint.pp(messages)
    pprint.pp(functions)

    result = chat.invoke(messages, functions=functions).additional_kwargs

    print(result)

    decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))

    with open("convcore/prompting/playground/playground_lch_result", "a") as p:
        p.write("\n")
        p.write(str(decoded_arguments))

    return decoded_arguments


def test_func_call():
    convo = [
        {"say": "moje oblíbené jídlo jsou špagety ale nemám moc rád psy", "who": "human"},
    ]

    prompts = [
        "vyjádřil svou lásku k psům",
        "sdílel, že nemá rád psy",
        "prozradil, že má hodně rád špagety",
        "zmínil, že špagety nepatří mezi jídla, která má rád",
    ]

    return intent_reco(prompts, convo)
