import sqlite3
import json

def list_items(args):
    flow = args.get("flow", "")
    item_type = args.get("item_type", "")

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flow WHERE flow_name = ?", (flow,))
    existing_record = cursor.fetchone()

    if not existing_record:
        return {
                "success": False,
                "message": f"flow {flow} doesnt exist"
            }

    conn.commit()
    conn.close()

    full_data = json.loads(existing_record[3])
    return {
        "success": True,
        "data": full_data
        }
