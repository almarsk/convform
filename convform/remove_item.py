import sqlite3
import json

def remove_item(args):
    flow = args.get("flow", "")
    item_type = args.get("item_type", "")
    name = args.get("name", "")

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flow WHERE flow_name = ?", (flow,))

    existing_record = cursor.fetchone()

    if existing_record :
        flow_data = json.loads(existing_record[3])

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


        for i, item in enumerate(items_list):
            if item.get("name", "").strip() == name.strip():
                items_list.pop(i)

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
                "message": f"from {flow} remove {name} of type {item_type}"
            }

    else:
        return {
            "success": False,
            "message": f"Can't remove from nonexistent flow {flow}"
        }
