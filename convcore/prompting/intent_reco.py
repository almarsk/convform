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
        'name': 'analyza_repliky_uzivatele',
        'description': '''\
For each parameter, consider whether it corresponds with the user speech. \
If it does, return 1 else return -1.\
Be strict. If the description is vague, remain skeptical. \
Only consider the last turn. The other ones are purely context''',
        'parameters': {
            'type': 'object',
            'properties': {
                f"{intent}": {
                    "type": "integer",
                    "description": f'''{prompt}''',
                    f"{intent}-why": {
                        "type": "string",
                        "description": f'''je pravda, že uživatel {prompt}? Proč anebo proč ne?'''
                    }
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
        print(decoded_arguments)
        return decoded_arguments
    else:
        return {}
