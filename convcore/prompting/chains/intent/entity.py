from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from convcore.prompting.utilz import api_key

import json
import pprint

def entity(prompts, convo, log):

    messages: list[HumanMessage | AIMessage | SystemMessage] = [
        SystemMessage(content=f"{turn['who']}: {turn['say']}")
        for turn in convo
    ]
    messages.insert(-1, SystemMessage(content="\nAktuální replika:"))

    # this is where multiple thread pool runs a chain on each to_match



def consider_match(message, prompt, log):
    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)

    messages = [SystemMessage(content=f"co je to entita? \
osoba, věc, předmět; nemusí být životné; \
většinou je to podstatné jméno a většina podstatných jmen jsou v promluvě entitou; \
podstatná jména, která v promluvě nejsou entitami jsou velmi obecná či časová; \
téma ve větě, ke kterému se dá odkázat osobním či vztažným zájmenem; \
promluva má většinou jednu entitu, občas dvě a málokdy více. \
nezřídka promluva entitu úplně postrádá. \
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
{message} \
\
Zvaž význam každého podstatného jména ve větě \
a zvaž, zda by mohlo představovat konkrétní entitu, a nejen abstraktní pojem. \
Uvažuj o všech možných objektech, které by mohly být v promluvě zmiňovány, \
a zvaž, zda by mohla být jejich jména považována za entity. \
\
U každého slova odůvodni svou úvahu a uzavři tím, že uvedeš slova vybraná jako entity. \
\
Jasně! Entity v uvedené větě jsou")]

    result = chat.invoke(messages)
    analysis = result.content

    functions=[{
        'name': 'input',
        'description': '''\
Na samotném závěru textu jsou zmíněná vybraná slova. Funkce se volá pomocí seznamu těchto slov. \
příklad: Takže v této větě není žádná entita, protože žádné z uvedených slov nepředstavuje konkrétní osobu, věc ani předmět. \
výstup: []
příklad: Entity v této větě jsou "klíč" a "rybník". \
výstup: ["klíč", "rybník"]''',
        'parameters': {
            'type': 'object',
            'properties': {
                f"chosen": {
                    "type": "list",
                    "description": f'''{prompt}'''
                }
            },
        'required': [f"chosen"]
    }}]

    result = chat.invoke([message], functions=functions)
    result = result.additional_kwargs

    if log:
        addition = [message, functions, result]
        log(addition)

    if "function_call" in result:
        decoded_arguments = json.loads(bytes(result["function_call"]["arguments"], "utf-8").decode("unicode_escape"))
        print("decoded", decoded_arguments)
        return {}
    else:
        return {}
