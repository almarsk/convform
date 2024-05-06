from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import json
import pprint

def entity(args):
    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)
    messages: list[HumanMessage | AIMessage | SystemMessage] = list()

    messages.append(SystemMessage(content=f"\
co je to entita? \
osoba, věc, předmět; \
nemusí být životné; \
většinou je to podstatné jméno a většina podstatných jmen jsou v promluvě entitou; \
podstatná jména, která v promluvě nejsou entitami jsou velmi obecná či časová; \
téma ve větě, ke kterému se dá odkázat osobním či vztažným zájmenem; \
promluva má většinou jednu entitu, občas dvě a málokdy více. nezřídka promluva entitu úplně postrádá. \
příklad: \
Alenku nejvíc baví vybika. \
Entity v této větě jsou Alenka a vybika. \
příklad: \
Nemám ráda sekanou. \
Entita v této větě je sekaná. \
příklad: \
Zas tak dlouho to netrvalo. \
Tato promluva postrádá entitu. \
příklad: \
Sraz máme zítra ve dvě. \
Tato promluva postrádá entitu. \
\
Na tomto základě zvaž, která slova jsou entity v následující větě: \
\
{args['speech']} \
\
Zvaž význam každého podstatného jména ve větě a zvaž, \
zda by mohlo představovat konkrétní entitu, \
a nejen abstraktní pojem. \
Uvažuj o všech možných objektech, které by mohly být v promluvě zmiňovány \
a zvaž, zda by mohla být jejich jména považována za entity. \
Občas je jediná entita reprezentována ve větě více slovy, třeba 'kamarád Pavel' je jedna entita. \
Pokud je větě nějaká entita vyjádřena více než jedním slovem, vyber důležitější z těchto slov jako entitu. \
\
U každého slova velmi stručně odůvodni svou úvahu a uzavři tím, že uvedeš slova vybraná jako entity. \
"))

    result = chat.invoke(messages)

    messages = [SystemMessage(content=result.content)]

    functions=[{
        'name': 'zaznam_entit',
        'description': f'''Zaznamenej, jestli uživatel zmínil nové entity.''',
        'parameters': {
            'type': 'object',
            'properties': {
                args["name"]: {
                    "type": 'boolean',
                    "description": f'''Zmínil uživatel nové entity?'''
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
        try:
            decoded_arguments = json.loads(result["function_call"]["arguments"])
            if args["name"] in decoded_arguments and decoded_arguments[args["name"]]:
                return {args["name"]: 0}
            else:
                return {args["name"]: -1}
        except:
            return {args["name"]: -1}


    return {args["name"]: -1}
