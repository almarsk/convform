import sqlite3
import json

def copy_item(args):
    from app import Reply, db

    flow = args.get("flow", "")
    item_type = args.get("item_type", "")
    name = args.get("name", "")

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
    target = [item for item in items if item["name"] == name]

    if not target:
        return {
            "success": True,
            "message": f"couldnt find {item_type} {name}"
        }

    copied_target = dict(target[0])
    split = copied_target["name"].split("_")

    if len(split) > 1 and split[-1].isdigit():
        new_name = "_".join(split[0:-1])
    else:
        new_name = copied_target["name"]

    index = 1
    while [item for item in items if item["name"] == new_name]:
        index += 1
        if len(split) > 1 and split[-1].isdigit():
            base = "_".join(split[0:-1])
        else:
            base = split[0]
        new_name = f"{base}_{str(index)}"

    copied_target["name"] = new_name

    flow_data[item_type+"s"].append(copied_target)

    cursor.execute('''UPDATE flow SET flow = ? WHERE flow_name = ?''',
        (json.dumps(flow_data), flow))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"copied {item_type} {name}"
    }
