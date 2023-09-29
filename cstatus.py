import convform
import json
import sys
import os
import sqlite3
import exp

# print("working dir: "+ os.getcwd())

class CStatusIn:
    def __init__(self, routine, superstate, user_reply, last_states, states_usage, turns_since_initiative):
        self.routine = routine
        self.superstate = superstate
        self.user_reply = user_reply
        self.last_states = last_states
        self.states_usage = states_usage
        self.turns_since_initiative = turns_since_initiative

def parse_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    routine = data.get('routine')
    superstate = data.get('superstate')
    user_reply = data.get('user_reply')
    last_states = data.get('last_states', [])
    states_usage = data.get('states_usage', {})
    turns_since_initiative = data.get('turns_since_initiative', 0)

    cstatus_instance = CStatusIn(
        routine,
        superstate,
        user_reply,
        last_states,
        states_usage,
        turns_since_initiative
    )

    return cstatus_instance

"""
if len(sys.argv) > 1:
    csi_name = sys.argv[1]
else:
    csi_name = "csi0"
csi_path = f"./convform_/bots/csi/{csi_name}.json"
csi = parse_json_file(csi_path)
"""

# print("csi: "+str(csi.__dict__))

"""
bot_path = "convform_/bots"
bot_name = "bohumil"

cso = convform.CStatusOut(bot_path, bot_name, csi)

cso.show()

print(cso.bot_reply)
print(cso.states_usage)
"""

def to_json(cso):
    q =  {"reply": cso.bot_reply,
        "meta":
            {
        "routine": cso.routine,
        "superstate": cso.superstate,
        "last_states": cso.last_states,
        "states_usage": cso.states_usage,
        "turns_since_initiative": cso.turns_since_initiative,
            }
    }
    j = json.dumps(q, ensure_ascii=False)
    #print("sql input: "+j)
    return j

def get_csi(user_id, user_reply):

    # exp.main(f"id={user_id}", True)

    conn = sqlite3.connect('chatbot.db')
    cursor_replies = conn.cursor()
    full_query = f"SELECT * FROM reply WHERE user_id = {user_id} AND cstatus IS NOT NULL ORDER BY id DESC LIMIT 1;" # cstatus is null in user replies

    cursor_replies.execute(full_query)
    most_recent_reply = cursor_replies.fetchall()

    if user_reply is None:
        user_reply = ""

    if len(most_recent_reply) > 0:
        current_cstatus = json.loads(json.loads(most_recent_reply[-1][-1]))
        current_cstatus["meta"]["user_reply"] = user_reply
        current_cstatus_user_reply = json.dumps(current_cstatus["meta"], ensure_ascii=False)
    else:
        current_cstatus_user_reply = json.dumps({
            "routine": "",
            "superstate": "",
            "user_reply": "",
            "last_states": [],
            "states_usage": {},
            "turns_since_initiative": 0,
        })
    cursor_replies.close()

    return current_cstatus_user_reply
