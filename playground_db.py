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

insert_data(cursor,("trefa", 1, load_json("bots/ink_pot_trefa.json"), 0, datetime.utcnow()))


# Commit changes and close connection
conn.commit()
conn.close()
