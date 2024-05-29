from langchain_openai import ChatOpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from convcore import api_key

with open("playground_lch_result", "a") as p:
    api_key()
    task=f"""
There is a conversation between A and B and there is a scale to rate from 1 to 3 on how much
the last turn makes sense in context of the previous turns. Your task is to produce the next turn {options[choice]}

The previous conversation:
    """
    chat = ChatOpenAI(model="gpt-4o", temperature=0.9)
    messages = list()
    messages.append(SystemMessage(content=task))
    messages.append(HumanMessage(content="Ahoj"))
    messages.append(AIMessage(content="Čau"))
    messages.append(HumanMessage(content="Nevíš jestli bude dneska pršet?"))
    messages.append(SystemMessage(content=f"""Your answer:

    Sure, an answering {options[choice]}"""))

    result = chat.invoke(messages)
    #print(result.content)
    p.write("\n")
    p.write(str(result.content))
