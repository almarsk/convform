import sqlite3
import json

def rename_item(args):
    from app import Reply, db

    # print(args)

    try:
        flow = args.get("flow", "")
        item_type = args.get("item_type", "")
        name = args.get("name", "")
        new_name = args.get("data", "")
    except:
        return {
            "success": False,
            "message": "wrong args"
        }

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flow WHERE flow_name = ?", (flow,))
    existing_record = cursor.fetchone()

    if not existing_record:
        return {
            "success": False,
            "message": f"couldnt find flow {flow}"
        }

    flow_data = json.loads(existing_record[3])
    items = flow_data[item_type+"s"]

    if [item for item in flow_data[item_type+"s"] if item["name"] == new_name]:
        return {
            "success": False,
            "message": f"{item_type} of name {new_name} already exists"
        }

    target = [item for item in items if item["name"] == name]

    if not target:
        return {
            "success": True,
            "message": f"couldnt find {item_type} {name}"
        }

    target[0]["name"] = new_name

    cursor.execute('''UPDATE flow SET flow = ? WHERE flow_name = ?''',
        (json.dumps(flow_data), flow))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"renamed {item_type} {name} to {new_name}"
    }
