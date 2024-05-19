from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import re
import json
import pprint
import time

def enstity(args, bench=False):
    start_time = 0
    if bench:
        start_time = time.time()

    chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, max_tokens=800)
    messages: list[HumanMessage | AIMessage | SystemMessage] = list()

    messages.append(SystemMessage(content=f"""\
Co je to entita? osoba, věc; nemusí být životné; \
Je to vždy podstatné jméno a většina podstatných jmen jsou v promluvě entitou; \
POZOR! Zájmena jako třeba "ty", "on" a podobně v žádném případě nikdy nejsou entity i pokud reprezentují osoby. \
slovesa určitě v žádném případě nejsou entitami ani pokud reprezentují osobu. \
podstatná jména, která v promluvě nejsou entitami jsou velmi obecná či časová; \
téma ve větě, ke kterému se dá odkázat osobním či vztažným zájmenem; \
promluva má většinou jednu entitu, občas dvě a málokdy více. nezřídka promluva entitu úplně postrádá.

příklad:
Alenku nejvíc baví vybika.
Entity v této větě jsou ["Alenka", "vybika"].
příklad:
Sraz máme zítra ve dvě.
Tato promluva postrádá entitu, výstup je tedy [].
příklad:
A co máš rád třeba ty?
Tato promluva postrádá entitu, přestože je v ní osobní zájmeno, výstup je tedy [].

Zvaž, která slova jsou entity v následující větě:

{args['speech']}

Zvaž význam každého podstatného jména ve větě a zvaž, zda by mohlo představovat konkrétní entitu, \
a ne jen abstraktní pojem. \
Uvažuj o všech možných objektech, které by mohly být v promluvě zmiňovány \
a zvaž, zda by mohla být jejich jména považována za entity. \
Nezapomeň, že slovesa ani zájmena nejsou entity, i když reprezentují osoby.

Velmi stručně odůvodni úvahu a uveď slova vybraná jako entity v hranatých závorkách ve fromátu JSON array. \
Nezapomeň úplně nakonci uvést JSON array s vybranými slovy."""))

    result = chat.invoke(messages).content

    if "log" in args:
        addition = [[str(message) for message in messages], result]
        args["log"]([args["chain"]])
        args["log"](addition)

    try:
        result = str(chat.invoke(messages).content)
        if bench:
            print(result)
        json_output = re.findall(str(r"\[.*\]"), result)

        if bench:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("elapsed:", elapsed_time, "seconds")
        entities = json.loads(json_output[-1])
        if bench:
            print(entities)

        if "log" in args:
            args["log"]([entities])
        if entities:
            return 0
        else:
            return -1
    except:
        return -1
