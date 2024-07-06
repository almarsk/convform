from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

import time

def basic(args, bench=False):
    messages = list()
    bot_intro = "Jasně, odpověď by mohla vypadat třeba takhle:"

    start_time = 0
    if bench:
        start_time = time.time()

    if args["persona"]:
        messages += [
            SystemMessage(content="persona: " + args["persona"])
        ]

    if args["context"] and not args["emphasis"]:
        messages += [SystemMessage(content="context:")]
        messages += [
            SystemMessage(content=f"{say['who']}: {say['say']}")
            for say in args["context"]
        ]

        messages+=[SystemMessage(content=f"""\
Robot {args["prompt"]} \
Vezme přitom v potaz předchozí konverzaci. \
Odpovídá stručně, jednou větou, maximálně 10 slov.

{bot_intro}""")]

    else:
        messages.append(SystemMessage(
            content=f"""Doplň další odpověď do konverzace.
Stručně, jednou větou, maximálně 10 slov.
Popis další odpovědi:
Robot {args["prompt"]}"""))

    try:
        chat = ChatOpenAI(model="gpt-4o", temperature=1)
        result = chat.invoke(messages)

        args["log"]([[m.content for m in messages], str(result.content)])

        if bench:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Elapsed time:", elapsed_time, "seconds")

        result_fin = str(result.content).strip("\"").strip("\'") if result.content else "Jejda, něco se pokazilo"

        # trying to get rid of the gpt intro if it does it
        return result_fin.split(bot_intro)[-1].strip()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Jejda, něco se pokazilo"
