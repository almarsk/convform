import json
import pprint
from functools import reduce

with open("notes/data/final_annotated_data.json", "r") as d:
    data = json.load(d)

    print(sum([c["rating"] or 5 for c in data if "rating" in c])/len(data))
    print(sum([c["rating"] for c in data if "rating" in c and c["rating"]])/len([c for c in data if "rating" in c and c["rating"]]))
