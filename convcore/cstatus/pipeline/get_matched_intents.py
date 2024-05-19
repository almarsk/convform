import sys
import re
from convcore.prompting.utilz import import_chains
from registered_chains import registered_chains
import pprint
from convcore.prompting.utilz import api_key

def get_matched_intents(pattern):
    prompt_done = False

    matches = list()


    for pattern_item in pattern["match_against"]:
        if pattern_item["prompt"] and not prompt_done:
            prompt_done = True
            matches.append((pattern["intent_name"],smart_match({
                "name": pattern["intent_name"],
                "prompt": pattern_item["text"],
                "chain": pattern_item["prompt"],
                "convo": pattern["history"],
                "log": pattern["log"],
                "speech": pattern["user_speech"],
            })))
        else:
            matches.append((pattern["intent_name"],string_match(pattern_item["text"], pattern["user_speech"])))

    if not matches:
        return None
    else:

       print(matches)

       lowest_index = sys.maxsize
       for (match_name, match_index) in matches:

           if match_index < 0:
               continue
           lowest_index = match_index if match_index < lowest_index else lowest_index
       if lowest_index < sys.maxsize and lowest_index >= 0:
           return {pattern["intent_name"]: {"index": lowest_index, "adjacent": pattern["adjacent"]}}
       else:
           return {}

def string_match(match_against, speech):

    match = re.search(match_against, speech)
    if match:
        start_index = match.start()
        return start_index
    else:
        return -1



def smart_match(args):
    api_key()
    return import_chains(registered_chains, "intent")[args["chain"]](args)
