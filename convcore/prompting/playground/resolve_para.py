from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import pprint
from concurrent.futures import ThreadPoolExecutor

def resolve(prompt, context):
    messages = list()
    last = "Co myslíš, bude dneska pršet?"
    if context:
        messages += [
            SystemMessage(content="Dosavadní konverzace:"),
            HumanMessage(content="Ahoj kamaráde"),
            AIMessage(content="Čau, rád tě vidím. To je dneska ale hezký jarní březnový den."),
            HumanMessage(content=last),
            SystemMessage(content=f"""\
Robot {prompt}.\
Vezme přitom v potaz informace v předchozí informaci a na základě nich odhadne nejlepší možnou odpověď.\
Odpovídá stručně, jednou větou, maximálně 10 slov.

Jasně, odpověď by mohla vypadat třeba takhle:""")]
    else:
        messages.append(SystemMessage(
            content=f"""There is a conversation
Your task is to give the next answer
The answer description:
{prompt}"""))

    try:
        chat = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
        result = chat.invoke(messages)

        with open("playground_lch_result", "a") as p:
            p.write("\n\n")
            p.write(str(result.content))

        return f'{str(result.content)}'
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

def resolve_para(prompts):

    with ThreadPoolExecutor() as exec:
        results = exec.map(resolve, *zip(*prompts))
        exec.shutdown(wait=True)  # Wait for all threads to finish

    return list(results)
