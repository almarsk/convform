import json
import pprint

with open("../final_annotated_data.json", "r") as d:
    data = json.load(d)


    result = {
        "success": 0,
        "fail": 0,
        "stimuli": {
            "shallow": {
                "success": 0,
                "fail": 0
            },
            "deep": {
                "success": 0,
                "fail": 0
            },
            "nonassignable": {
                "success": 0,
                "fail": 0
            }
        }
    }


    for d in data:
        if "stimulus" not in d or "type" not in d:
            continue

        annotated = d["stimulus"]
        intended = d["type"]

        success = False
        if annotated in intended:
            success = True
        result["success" if success else "fail"] += 1

        if success:
            result["stimuli"][annotated]["success"] += 1
        else:
            for key in result["stimuli"].keys():
                if key in intended:
                    result["stimuli"][key]["fail"] += 1


pprint.pp(result)
