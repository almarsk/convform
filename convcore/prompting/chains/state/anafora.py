from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains.state.basic import basic

def anafora(args):
    answer = basic(args)

    messages = [
        SystemMessage(content="najdi ve větě jedno hlavní slovo, o kterém věta je a vyměň ho za osobní nebo vztažné zájmeno. Ostatní tematická centra nech jak jsou."),
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
