import json
import sqlite3
from datetime import datetime
import pprint


conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# pprint.pp([q for q in cursor.execute('''SELECT * FROM Flow;''')])
# pprint.pp([x for x in cursor.execute('''SELECT * FROM Reply;''')])
# pprint.pp([x for x in cursor.execute('''SELECT * FROM Conversation;''')])
# Insert JSON data into SQLite database
#
def load_json(file_path):
     with open(file_path, 'r') as file:
         data = json.load(file)
     return json.dumps(data)

def insert_data(cursor, data):
     cursor.execute('''INSERT INTO Flow (flow_name, project_id, flow, is_archived, created_on)
                            VALUES (?, ?, ?, ?, ?)''',
                            data)

for bot in [
    "f_AutoMarta-sh-rel.json",
    "f_Elizabota-sh-inq.json",
    "f_Ondroid-un-inq.json",
    "f_Vladimatik-un-rel.json"
]:
    insert_data(cursor,(bot.strip(".json"), 1, load_json(f"bots/exp1/{bot}"), 0, datetime.utcnow()))


# Commit changes and close connection
conn.commit()
conn.close()
