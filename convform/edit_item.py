import sqlite3
import json
from slugify import slugify

def edit_item(args):
    from app import Flow, db

    flow = args.get("flow", "")
    item_type = args.get("item_type", "")
    name = slugify(args.get("name", ""))
    data = args.get("data", "")
    if "name" in data:
        data["name"] = name

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flow WHERE flow_name = ?", (flow,))
    existing_record = cursor.fetchone()

    if existing_record :
        flow_data = json.loads(existing_record[3])

        if item_type == "meta":
            for key, value in data.items():
                if key != "states" and key != "intents":
                    flow_data[key] = value

        else:
            items_list = None
            if item_type == "intent":
                items_list = flow_data.get("intents", [])
            elif item_type == "state":
                items_list = flow_data.get("states", [])
            if items_list is None:
                return {
                    "success": False,
                    "message": f"Invalid item type {item_type}"
                }

            updated = False
            for item in items_list:
                if item.get("name", "").strip() == name.strip():
                    if not isEdited(data):
                        return {
                            "success": False,
                            "message": f"{item_type} {name} already in {flow}"
                        }
                    item.update(data)
                    updated = True
            if not updated:
                items_list.append(data)

            if item_type == "intent":
                flow_data["intents"] = items_list
            elif item_type == "state":
                flow_data["states"] = items_list

        cursor.execute('''UPDATE flow SET flow = ? WHERE flow_name = ?''',
            (json.dumps(flow_data), flow))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"{item_type} {name} edited in {flow}"
        }

    else:
        return {
            "success": False,
            "message": f"Can't edit nonexistent flow {flow}"
        }

def isEdited(data):
    updatedData = False
    for key, value in data.items():
        if key == "name":
            pass
        elif value:
            updatedData = True
    return updatedData
