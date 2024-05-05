import sys
import re
from convcore.prompting.utilz import import_chains, match_prompt_intents
from registered_chains import registered_chains
import pprint
from convcore.prompting.utilz import api_key

def get_matched_intents(pattern):
    prompt_done = False

    matches = list()

    for pattern_item in pattern["match_against"]:
        if pattern_item["prompt"] and not prompt_done:
            prompt_done = True
            matches.append(smart_match({
                "name": pattern["intent_name"],
                "prompt": pattern_item["text"],
                "chain": pattern_item["prompt"],
                "convo": pattern["history"],
                "log": pattern["log"],
                "speech": pattern["user_speech"],
            }))
        else:
            matches.append(string_match(pattern_item["text"], pattern["user_speech"]))

    return {}


    """





            else:
                match_info = is_match(match_against["text"], user_speech)
                if match_info["is_match"]:
                    matched = True
                    if match_info["match_index"] < match_index:
                        match_index = match_info["match_index"]

        if matched:
            matched_intents_with_start_index[intent] = match_index

    print("tomatch2", prompts_to_match)
    # do the prompting
    matched_prompts = dict()
    if prompts_to_match:
        matched_prompts = match_prompt_intents({
            "prompts": prompts_to_match, "history": history, "log": log})

    # add llm matched intents to matched_intents_with_start_index
    for intent, index in matched_prompts.items():
        # find intent based on prompt
        if index >= 0:
            matched_intents_with_start_index[intent] = index

    #print(matched_prompts)
    #print("matched llm",matched_intents_with_start_index)

    return matched_intents_with_start_index

   """

def string_match(match_against, speech):
    match = re.search(match_against, speech)
    if match:
        start_index = match.start()
        return {
            "is_match": True,
            "match_index": start_index
        }
    else:
        return {
            "is_match": False,
            "match_index": sys.maxsize
        }



def smart_match(args):
    api_key()
    pprint.pp(args)
    import_chains(registered_chains, "intent")[args["chain"]](args)
