from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import json
import pprint

from convcore.prompting.utilz import api_key

def entity():
    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)
    messages: list[HumanMessage | AIMessage | SystemMessage] = list()


    messages = [SystemMessage(content='''V této větě "no už jsem docela dlouho nebyl a dělá mi to dobře zvedat činky" můžeme identifikovat následující podstatná jména: "činky".
- "činky" - Toto slovo představuje konkrétní předmět, který je používán při fyzické aktivitě. V této větě je to konkrétní entita, na kterou se může odkazovat a která má specifický význam v kontextu promluvy.
Slova jako "dlouho" nebo "dobře" jsou příslovce nebo abstraktní pojmy, které samy o sobě nepředstavují entitu. "No" je částice a "už", "docela", "nebyl", "a", "dělá", "mi", "to" jsou slova, která neoznačují konkrétní objekty nebo osoby.
Na základě této analýzy jsou slova vybraná jako entity v této větě: "činky".''')]

    functions=[{
        'name': 'zaznam_entit',
        'description': f'''Funkce zaznemanává, které nové entity uživatel zmínil podle analýzy. Vrací prázdný řetězec, pokud žádné nové entity nezmínil.''',
        'parameters': {
            'type': 'object',
            'properties': {
                "anafora-op": {
                    "type": 'boolean',
                    "description": f'''Zmínil uživatel nové entity'''
                }
            },
        'required': ["anafora-op"]
    }}]

    result = chat.invoke(messages, functions=functions)
    result = result.additional_kwargs

    print(result["function_call"]["arguments"])

    if "function_call" in result:
        decoded_arguments = json.loads(result["function_call"]["arguments"])
        print(decoded_arguments)
