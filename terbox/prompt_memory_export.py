import sqlite3
import re
from langchain.schema import AIMessage, HumanMessage

def update_memory(user_id, memory):
    conn = sqlite3.connect('chatbot.db')
    cursor_replies = conn.cursor()
    cursor_replies.execute(f"SELECT * FROM reply WHERE user_id = {user_id};")
    replies = cursor_replies.fetchall()

    for reply in replies:
        print(reply)
        if reply[4]: # duration - is only measured for user
            memory.append(HumanMessage(content=reply[2].strip()))
        else:
            memory.append(AIMessage(content=reply[2].strip()))


    cursor_replies.close()
    conn.close()
