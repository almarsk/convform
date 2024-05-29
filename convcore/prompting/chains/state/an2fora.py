from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

def anafora(args, bench=False):
    answer = basic(args, bench)

    messages = [
        SystemMessage(content="""\
úkol:
najdi ve větě jedno hlavní slovo, o kterém věta je a vyměň ho za osobní nebo vztažné zájmeno. Ostatní tematická centra nech jak jsou. Nezapomeň také vynechat slova, která jsou případně součástí jmenné fráze nahrazovaného slova. Nezapomeň také, že v případě nahrazení podstatného jména zájmenem je často třeba změnit slovosled - sloveso pak bude často až na konci věty; je třeba dodržet pořadí příklonek - nahrazovací zájmeno přijde pro zvratném a osobním zájmeně. Je také třeba správně rozeznat důležitější slovo - vol to, o kterém je otázka.

příklad1:
věta:
A o čem bude tvoje seminárka?
úvaha:
nahrazované slovo bude seminárka. slovo "tvoje" patří do jmenné fráze nahrazovaného slova.
tvoje odpověď:
A o čem ona bude?

příklad2:
věta:
jak daleko od tvého domu je tvůj oblíbený park?
úvaha:
nahrazované slovo bude "park", je ve větě důležitější než slovo "domu". slovo "tvůj" patří do jmenné fráze nahrazovaného slova stejně jako slovo "oblíbený".
tvoje odpověď:
jak daleko od tvého odmu on je?

úvahu vynech."""),
        SystemMessage(content="věta:"),
        SystemMessage(content=answer),
        SystemMessage(content="Jasně! Upravená věta bez speciálního formátování bude vypadat takhle:")
    ]
    try:
        chat = ChatOpenAI(model="gpt-4o", temperature=0.3)
        result = chat.invoke(messages)
        args["log"]([[m.content for m in messages], str(result.content)])
        return str(result.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
