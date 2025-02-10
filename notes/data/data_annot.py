import json
import csv
import pprint

with open("export/final_data.json", "r") as d:
    data = json.load(d)

with open("export/final-data.json", "r") as dp:
    data_prompt = json.load(dp)

with open("export/chatbot anotace - List 1.csv", "r") as a:



    final_annotated_data = list()
    design = dict()

    for bot, data in data.items():
        design[bot] = data["type"]

        for convo_id, convo_data in data["data"].items():


            a.seek(0)
            annotation = csv.reader(a)
            next(annotation)

            for line in annotation:

                print(line)
                if line[0] == convo_id:
                    convo_data["stimulus"] = line[1]
                    convo_data["user_reaction"] = line[2] if line[2] else "continuation"
                    convo_data["comment_annot"] = line[3]
                    convo_data["generation_issue"] = True if line[4] == "TRUE" else False
                    convo_data["zero_anaphore"] = True if line[5] == "TRUE" else False
                    break



            if convo_id in data_prompt[bot]["data"]:
                for meta in data_prompt[bot]["data"][convo_id]["conversation_meta"]:
                    if meta["stimuli"]:
                        # print("id",convo_id)
                        # pprint.pp(meta)
                        convo_data["stimulus_prompt"] = meta["prompting"]
                        convo_data["stimulus_entities"] = meta["entities"]
                        break

            convo_data.pop("nick")
            convo_data["id"] = convo_id
            convo_data["type"] = design[bot]
            final_annotated_data.append(convo_data)

#pprint.pp(final_annotated_data)

with open("export/final_annotated_data.json", "w", encoding="utf-8") as json_file:
    json.dump(final_annotated_data, json_file, indent=4, ensure_ascii=False)
