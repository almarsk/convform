import json
import random
import re
from typing import Tuple, Any


def get_flow_json(flow_name) -> dict:
    try:
        with open(f"flows/{flow_name}.json", "r") as k:
                flow = json.load(k)
                return flow
    except FileNotFoundError:
        print("File not found")
        return {FileNotFoundError: "ajaj, ta moje hlava děravá, jsem nějaký rozbitý"}
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return {json.JSONDecodeError: "ajaj, nějak nevím, co jsem to chtěl říct, jsem nějaký rozbitý"}
    except Exception as e:
        print("An error occurred:", str(e))
        return {Exception: "ajaj něco se nepovedlo, jsem nějaký rozbitý"}

def find_matches(state_intents, state_iterations, user_reply):
    matched_intents = []
    for intent in state_intents:
        current_intent = state_intents[intent]

        for item in current_intent["keywords"]:
            if re.search(item.lower(), user_reply.lower()):
                state_iterations.setdefault(intent, 0)
                state_iterations[intent] += 1
                matched_intents.append(intent)
    return matched_intents


def sort_intents_priority(matched_intents, state_intents):
        matched_intents.sort(key=lambda intent: state_intents[intent]["priority"], reverse=True)
        return matched_intents


def extract_overiterated(matched_intents, state_intents, intent_iterations) -> Tuple[list, list]:
    iterating_intents = []
    # over-iterated intents are taken out of the list
    print("matched: "+str(matched_intents))
    for possible_intent in list(matched_intents):
        print(possible_intent+" "+str(intent_iterations[possible_intent]))
        print(possible_intent+" "+str(state_intents[possible_intent]["iteration"]))
        if intent_iterations[possible_intent] > state_intents[possible_intent]["iteration"]:
            iterating_intents.append(matched_intents.pop(matched_intents.index(possible_intent)))
            print("non_over: "+str(matched_intents)+ " over: "+str(iterating_intents))
    return (matched_intents, iterating_intents)


def annotated_intents_dict(matched_intents, iterating_intents):
    pass


def append_answers(intents_group: list, final_picked_answer_list: list, state_intents, over_iterated: bool):
    if len(intents_group):
        source_text = "over_iterated_answers" if over_iterated else "answers"
        for intent in intents_group:
            answer_list = state_intents[intent][source_text]
            final_picked_answer_list.append(answer_list[random.randint(0, len(answer_list)-1)])


def get_answer(matched_iterating_intents, state_intents):
    final_picked_answer_list = []
    append_answers(matched_iterating_intents[0], final_picked_answer_list, state_intents, over_iterated = False)
    append_answers(matched_iterating_intents[1], final_picked_answer_list, state_intents, over_iterated = True)
    return final_picked_answer_list[0]


def fallback_response(fallback):
    return fallback[random.randint(0, len(fallback)-1)]
