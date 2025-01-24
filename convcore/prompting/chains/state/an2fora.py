from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

def an2fora(args, bench=False):

    bot_intro= "Jasně! Upravená věta bez speciálního formátování bude vypadat takhle:"
    topic = None
    # coming from b_dynamic
    if "about_what" in args:
        topic = args["about_what"]
    elif "entities_all" in args:
        try:
            topic = args["entities_all"][-2][-1]
            # change for a call which specifies what to ask about
            args["prompt"] = f"se položí doplňující otázku k tématu {topic}."
        except:
            pass


    # print("prompt", args["prompt"])
    answer = basic(args, bench)
    input = list()

    task = ("najdi ve větě jedno hlavní slovo a vyměň ho za anaforu - třeba osobní nebo vztažné zájmeno, zájmenné příslovce nebo v případě potřeby nulovou anaforu (tedy nic)."
        if not topic
        else f"slovo {topic} ve vyměň za anaforu - osobní nebo vztažné zájmeno, zájmenné příslovce nebo v případě potřeby nulovou anaforu (tedy nic).")

    # print("task", task)

    input += [
        SystemMessage(content=f"""\
úkol: \
{task} \
Ostatní tematická centra nech jak jsou. \
Nezapomeň také vynechat slova, která jsou případně součástí jmenné fráze nahrazovaného slova. \
Nezapomeň také, že v případě nahrazení podstatného jména zájmenem je často třeba změnit slovosled - \
sloveso pak bude často až na konci věty; je třeba dodržet pořadí příklonek - \
nahrazovací zájmeno přijde pro zvratném a osobním zájmeně. Je také třeba správně rozeznat důležitější slovo - \
vol to, o kterém je otázka. \
Pro zachování přirozenosti je občas potřeba taky upravit větu tak, \
že obsahuje vedlejší větu, obzvlášť pokud je nahrazované slovo navázané na deverbativní podstatné jméno.
Někdy je potřeba trochu změnit slovosled věty.
Zhodnoť jestli je přirozenější nulová nulová nebo explicitní anafora.

příklad1:
věta:
A o čem bude tvoje seminárka?
úvaha:
nahrazované slovo bude seminárka. slovo "tvoje" patří do jmenné fráze nahrazovaného slova.
tvoje odpověď:
A o čem bude?

příklad2:
věta:
jak daleko od tvého domu je tvůj oblíbený park?
úvaha:
nahrazované slovo bude "park", je ve větě důležitější než slovo "domu". slovo "tvůj" patří do jmenné fráze nahrazovaného slova stejně jako slovo "oblíbený".
tvoje odpověď:
jak daleko od tvého domu je?

příklad3:
kontext:
půjdu do kavárny
věta:
jaká je tvoje oblíbená káva v té kavárně?
úvaha:
nahrazované slovo bude "kavárně", kvůli jeho finální pozici ve větě. kvůli přirozenému slovosledu bude potřeba nahrazovací zájmeno předsunout.
tvoje odpověď:
jaká je tam tvoje oblíbená káva?

příklad4:
věta:
Na jaké trati tě nejvíc baví závodit?
tvoje odpověď:
Na které tě nevíc baví závodit?

úvahu vynech."""),
        SystemMessage(content="věta:"),
        SystemMessage(content=answer),
        SystemMessage(content=bot_intro)
    ]
    try:
        chat = ChatOpenAI(model="gpt-4o", temperature=0.3)
        result = chat.invoke(input)
        args["log"]([[m.content for m in input], str(result.content)])
        result_fin = str(result.content)
        # this checks that gpt didnt return the given intro
        return result_fin.split(bot_intro)[-1].strip()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
