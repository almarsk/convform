import json
import pprint
from functools import reduce

with open("export/final_annotated_data.json", "r") as d:
    data = json.load(d)


    print(f"Number of convos: {len(data)}")

    zero_anaphora_number = len([convo for convo in data if 'zero_anaphora' in convo and convo['zero_anaphora']])
    print(f"Number of zero anaphora conversations: {zero_anaphora_number}")


    def get_rating_avg(stimulus_type: str):
        _rated = [c["rating"] for c in data if "rating" in c and c["rating"] and "type" in c and stimulus_type in c["type"]]
        _sum_score = sum([c for c in _rated])
        rating_avg = _sum_score/len(_rated)
        print(f"Rating {stimulus_type} {rating_avg}")

    get_rating_avg("shallow")
    get_rating_avg("deep")
    get_rating_avg("nonassignable")
