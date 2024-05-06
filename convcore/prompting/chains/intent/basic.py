from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import json
import pprint

def basic(args):
    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)

    messages: list[HumanMessage | AIMessage | SystemMessage] = [
        HumanMessage(content=turn["say"])
        if turn["who"] == "human"
        else AIMessage(content=turn["say"])
        for turn in args["convo"]
    ]

    messages.insert(-1, SystemMessage(content="\nAktuální replika:"))
    messages.append(HumanMessage(content=f"Zajímalo by mě, jestli uživatel {args['prompt']}"))

    functions=[{
        'name': 'analyza_repliky_uzivatele',
        'description': f'''Funkce zaznemanává, jestli uživatel {args["prompt"]}''',
        'parameters': {
            'type': 'object',
            'properties': {
                args["name"]: {
                    "type": "boolean",
                    "description": f'''je pravda, že uživatel {args["prompt"]}?'''
                }
            },
        'required': [args["name"]]
    }}]

    result = chat.invoke(messages, functions=functions)
    result = result.additional_kwargs

    addition = [[str(message) for message in messages], functions, result]
    args["log"]([args["chain"]])
    args["log"](addition)

    if "function_call" in result:
        decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))
        if args["name"] in decoded_arguments and decoded_arguments[args["name"]]:

            messages = [HumanMessage(content=f"Zajímalo by mě, jestli uživatel {args['prompt']}")]
            functions=[{
                'name': 'zaznam_segmentu_repliky',
                'description': f'''Funkce zaznemanává, na jakém indexu v replice uživatel {args["prompt"]}''',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        args["name"]: {
                            "type": "integer",
                            "description": f'''na jaké indexu v aktuální replice uživatel {args["prompt"]}?'''
                        }
                    },
                'required': [args["name"]]
            }}]

            result = chat.invoke(messages, functions=functions)
            result = result.additional_kwargs
            addition = [[str(message) for message in messages], functions, result]
            args["log"](addition)

            if "function_call" in result:
                decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))

                return decoded_arguments

    return {args["name"]: -1}
