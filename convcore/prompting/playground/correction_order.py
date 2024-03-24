from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from convcore import api_key

import json
import pprint

def correction_order():
    api_key()

    chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)

    messages= [SystemMessage(content="""Instrukce:
    Následuje replika jednoho mluvčího. zkontroluj, že její jednotlivé části jsou seřazené správně a přirozeně a pokud ne, seřaď je lépe.

    Uvažuj například takhle:
    pozdrav by měl být jako první,
    otázka by měla být jako poslední,
    různé poznámky a komentáře by měly být seřazeny tak aby na sebe navazovaly,
    uvození tématu nebo vyprávění musí předcházet rozvedení tématu nebo vyprávění
    a tak dál

    Replika:
    Ahoj jmenuju se Beruška  ráda tě poznávám. Dostali jsme tam dort, protože můj spolužák měl narozeniny. Musím ti povědět, co se dnes dělo ve škole.

    Tvoje seřazení:
    jasně, zkontroluji a případně lépe seřadím repliku! šlo by to třeba takhle:""")]


    result = chat.invoke(messages)


    with open("convcore/prompting/playground/playground_lch_result", "a") as p:
        p.write("\n")
        p.write(str(result.content))

    return result.content




correction_order()
