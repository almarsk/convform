from langchain_core import messages
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

from convcore.prompting.chains import basic

def anafora(args):
    answer = basic(args)

    messages = [
        SystemMessage(content="najdi ve větě hlavní jmennou frázi a vyměň ji za osobní nebo vztažné zájmeno. Pokud to nejde, vrať ji tak, jak je."),
        SystemMessage(content="věta:"),
        SystemMessage(content=answer),
        SystemMessage(content="Jasně! Když v této větě vyměním hlavní jmennou frázi za osobní nebo vztažné zájmeno \
            věta bude vypadat takhle:")
    ]
    try:
        chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.3)
        result = chat.invoke(messages)
        args["log"]([[m.content for m in messages], str(result.content)])
        #print(f'anafora {str(result.content)}')
        return str(result.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
