import sys
import re
from convcore.prompting.intent_reco import intent_reco

def get_matched_intents(flow, to_match_intent_names, user_speech, history, log):
    get_full_intent = lambda searched_intent: [
        intent
        for intent in flow.intents
        if intent.name == searched_intent
    ][0]

    matched_intents_with_start_index = dict()
    prompts_to_match = list()

    for intent in to_match_intent_names:
        full_intent = get_full_intent(intent)

        matched = False
        match_index = sys.maxsize

        for match_against in full_intent.match_against:

            if match_against["prompt"]:
                # add prompt to call llm later
                prompts_to_match.append(
                    {"prompt": match_against["text"], "intent": intent}
                )
            else:
                match_info = is_match(match_against["text"], user_speech)
                if match_info["is_match"]:
                    matched = True
                    if match_info["match_index"] < match_index:
                        match_index = match_info["match_index"]

        if matched:
            matched_intents_with_start_index[intent] = match_index

    # do the prompting
    prompts = {prompt["intent"]: prompt["prompt"] for prompt in prompts_to_match}
    matched_prompts = dict()
    if prompts:
        matched_prompts = intent_reco(prompts, history, log)

    # add llm matched intents to matched_intents_with_start_index
    for intent, index in matched_prompts.items():
        # find intent based on prompt
        if index >= 0:
            matched_intents_with_start_index[intent] = index

    #print(matched_prompts)
    #print("matched llm",matched_intents_with_start_index)

    return matched_intents_with_start_index


def is_match(match_against, speech):
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
