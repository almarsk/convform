from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

def an2fora(args, bench=False):
    answer = basic(args, bench)
    input = list()

    if args["context"] and not args["emphasis"]:
        input += [SystemMessage(content="context:")]
        input += [
            SystemMessage(content=f"{say['who']}: {say['say']}")
            for say in args["context"]
        ]


    input += [
        SystemMessage(content="""\
úkol: \
najdi ve větě jedno hlavní slovo, které větu spojuje s kontextem a vyměň ho za osobní nebo vztažné zájmeno. \
Ostatní tematická centra nech jak jsou. \
Nezapomeň také vynechat slova, která jsou případně součástí jmenné fráze nahrazovaného slova. \
Nezapomeň také, že v případě nahrazení podstatného jména zájmenem je často třeba změnit slovosled - \
sloveso pak bude často až na konci věty; je třeba dodržet pořadí příklonek - \
nahrazovací zájmeno přijde pro zvratném a osobním zájmeně. Je také třeba správně rozeznat důležitější slovo - \
vol to, o kterém je otázka.

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

příklad3:
kontext:
půjdu do kavárny
věta:
jaká je tvoje oblíbená káva v té kavárně?
úvaha:
nahrazované slovo bude "kavárně", protože se nachází v kontextu. kvůli přirozenému slovosledu bude potřeba nahrazovací zájmeno předsunout.
tvoje odpověď:
jaká je v ní tvoje oblíbená káva?

úvahu vynech."""),
        SystemMessage(content="věta:"),
        SystemMessage(content=answer),
        SystemMessage(content="Jasně! Upravená věta bez speciálního formátování bude vypadat takhle:")
    ]
    try:
        chat = ChatOpenAI(model="gpt-4o", temperature=0.3)
        result = chat.invoke(input)
        args["log"]([[m.content for m in input], str(result.content)])
        return str(result.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
