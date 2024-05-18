from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from convcore import api_key

import json
import pprint

def intent_reco(prompts, convo):
    api_key()

    chat = ChatOpenAI(model="gpt-4o", temperature=0.5)

    messages: list[HumanMessage | AIMessage | SystemMessage] = [
        HumanMessage(content=turn["say"])
        if turn["who"] == "human"
        else AIMessage(content=turn["say"])
        for turn in convo
    ]

    messages.insert(-1, SystemMessage(content="\nAktuální replika:"))

    functions=[{
        'name': 'zhodnot_nalezitost_popisu',
        'description': '''\
Zaznamenej u jednotlivých popisů,\
jestli odpovídají aktuální replice v konverzaci.\
Hodnoť jen poslední repliku, \
ty předchozí jsou zde jen pro kontext''',
        'parameters': {
            'type': 'object',
            'properties': {
                f"popis{index}": {
                    "type": "boolean",
                    "description": "uživatel v aktuální replice "+prompt,
                } for index, prompt in enumerate(prompts, start=1)
            },
        'required': [f"popis{index}" for index, _ in enumerate(prompts, start=1)]
    }}]

    pprint.pp(messages)
    pprint.pp(functions)

    result = chat.invoke(messages, functions=functions).additional_kwargs
    decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))

    with open("convcore/prompting/playground/playground_lch_result", "a") as p:
        p.write("\n")
        p.write(str(decoded_arguments))

    return decoded_arguments


def test_func_call():

    convo = [
        {"say": "Ahoj, jak se máš", "who": "human"},
        {"say": "čau jo dobře, mám se fajn. co teď děláš?", "who": "bot"},
        {"say": "dneska je ošklivo", "who": "human"},
    ]

    prompts = [
        "prozradil co dělá",
        "zeptal se bota jak se má",
        "postěžoval si na počasí",
        "pochválil počasí",
    ]

    return intent_reco(prompts, convo)
