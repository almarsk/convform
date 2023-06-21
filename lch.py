import sqlite3
import json
from langchain.memory import ConversationBufferMemory
from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def apiKey():
    with open("config.json", "r") as c:
        config = json.load(c)
        return config["openai_api_key"]

def fillUpMem(cState, memory: ConversationBufferWindowMemory):
    print("stav",cState)
    user_id= cState["user_id"]
    print("uíd",type(user_id)," ",user_id)
    conn = sqlite3.connect('chatbot.db')
    cursor_replies = conn.cursor()
    cursor_replies.execute(f"SELECT * FROM reply WHERE user_id == {user_id};")
    replies = cursor_replies.fetchall()
    if len(replies):
        memory.chat_memory.add_ai_message(replies[0][2])
        for i in range(1, len(replies), 2):
            if i+1 < len(replies):
                memory.save_context({"input": replies[i][2]}, {"output": replies[i + 1][2]})

async def smart_reply(cState, user_reply):
    template ="""Jmenuješ se Zvědavobot a jsi česky mluvící robot.
Mluvíš v krátkých větách.
Když je to vhodné a co nejvíc používáš metakomunikační fráze.
{history}
{input}
AI:"""

    prompt = PromptTemplate(
        input_variables=['history', 'input'],
        partial_variables={},
        template=template
    )

    memory = ConversationBufferWindowMemory(human_prefix="Kamarád", k=5)
    fillUpMem(cState, memory)
    llm = ChatOpenAI(openai_api_key=apiKey(), model_name= "gpt-3.5-turbo", temperature=0, client=None)
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )
    try:
        response: str = conversation.run(f"Kamarád: {user_reply}" if user_reply else " ")
        return response
    except:
        return ""
