import json
import sqlite3
from datetime import datetime
import pprint


conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# pprint.pp([q for q in cursor.execute('''SELECT * FROM Flow;''')])
# pprint.pp([x for x in cursor.execute('''SELECT * FROM Reply;''')])
pprint.pp([x for x in cursor.execute('''SELECT * FROM Conversation;''')])
# Insert JSON data into SQLite database
# insert_data(cursor,("brlb", 1, load_json("bots/brlb.json"), 0, datetime.utcnow()))


# Commit changes and close connection
conn.commit()
conn.close()
