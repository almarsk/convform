from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

def an2fora(args):
    answer = basic(args)
    messages= []

    if args["context"]:
        last_turn = args["context"][-1]
        messages += [SystemMessage(content="poslední odpověď uživatele:"),
            SystemMessage(content=f"{last_turn['who']}: {last_turn['say']}")
        ]

    messages += [
        SystemMessage(content="\
slovo, které spojuje větu s kontextem nahraď osobním nebo vztažným zájmenem. \
Určitě proveď záměnu, odstranit slovo nestačí, je nutné osobní nebo vztažné zájmeno přidat. \
Pokud tam není doslovně, osobní nebo vztažné zájemno přidej. \
Ostatní tematická centra nech jak jsou."),
        SystemMessage(content="věta:"),
        SystemMessage(content=answer),
        SystemMessage(content="Jasně! Upravená věta bude vypadat takhle:")
    ]
    try:
        chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.3)
        result = chat.invoke(messages)
        args["log"]([[m.content for m in messages], str(result.content)])
        return str(result.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
