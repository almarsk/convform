from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import re
import json
import pprint
import time

def entity(args, bench=False):
    start_time = 0
    if bench:
        start_time = time.time()

    chat = ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=0, max_tokens=200)
    messages: list[HumanMessage | AIMessage | SystemMessage] = list()

    messages.append(SystemMessage(content=f"""\
co je to entita? osoba, věc, předmět; nemusí být životné; \
slovesa určitě v žádném případě nejsou entitami ani pokud reprezentují osobu. \
většinou je to podstatné jméno a většina podstatných jmen jsou v promluvě entitou; \
podstatná jména, která v promluvě nejsou entitami jsou velmi obecná či časová; \
téma ve větě, ke kterému se dá odkázat osobním či vztažným zájmenem; \
promluva má většinou jednu entitu, občas dvě a málokdy více. nezřídka promluva entitu úplně postrádá.

příklad:
Alenku nejvíc baví vybika.
Entity v této větě jsou Alenka a vybika.
příklad:
Nemám ráda sekanou.
Entita v této větě je sekaná.
příklad:
Zas tak dlouho to netrvalo.
Tato promluva postrádá entitu.
příklad:
Sraz máme zítra ve dvě.
Tato promluva postrádá entitu.

Na tomto základě zvaž, která slova jsou entity v následující větě:

{args['speech']}

Zvaž význam každého podstatného jména ve větě a zvaž, zda by mohlo představovat konkrétní entitu, \
a ne jen abstraktní pojem. \
Uvažuj o všech možných objektech, které by mohly být v promluvě zmiňovány \
a zvaž, zda by mohla být jejich jména považována za entity. \
Nezapomeň, že slovesa nejsou entity, i když reprezentují osoby.

Velmi stručně odůvodni úvahu a uzavři tím, \
že uvedeš slova vybraná jako entity v hranatých závorkách ve fromátu JSON array. \
Nezapomeň úplně nakonci uvést JSON array s vybranými slovy.

Jasně! Entity v uvedené větě jsou"""))

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
        entities = json.loads(json_output[-1])
        if bench:
            print(entities)

        if bench:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("elapsed:", elapsed_time, "seconds")

        if "log" in args:
            args["log"]([entities])
        if entities:
            return {args["name"]: 0}
        else:
            return {args["name"]: -1}
    except:
        return {args["name"]: -1}
