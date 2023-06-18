import json
import random
import re
from typing import Tuple, Any
import os


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
        matched_intents.sort(key=lambda intent: state_intents[intent]["priority"])
        return matched_intents


def extract_overiterated(matched_intents, state_intents, intent_iterations) -> Tuple[list, list]:
    iterating_intents = []
    # over-iterated intents are taken out of the list
    for possible_intent in list(matched_intents):
        if intent_iterations[possible_intent] > state_intents[possible_intent]["iteration"]:
            iterating_intents.append(matched_intents.pop(matched_intents.index(possible_intent)))
    return (matched_intents, iterating_intents)


def annotated_intents(assorted_intents):
    annotated_intents = []
    matched_intents = assorted_intents[0]
    overiterated_intents = assorted_intents[1]
    for intent in matched_intents:
        annotated_intents.append([intent, 0])
    for intent in overiterated_intents:
        annotated_intents.append([intent, 1])
    return annotated_intents


def append_answers(intents_group: list, final_picked_answer_list: list, state_intents, over_iterated: bool):
    if len(intents_group):
        source_text = "over_iterated_answers" if over_iterated else "answers"
        for intent in intents_group:
            answer_list = state_intents[intent][source_text]
            final_picked_answer_list.append(answer_list[random.randint(0, len(answer_list)-1)])


def compose_answer(assorted_intents, state_intents) -> str:
    # only over-iterated
    if not len(assorted_intents[0]) and len(assorted_intents[1]):
        answer_list = state_intents[assorted_intents[1][0]]["over_iterated_answers"]
        random_answer = answer_list[random.randint(0, len(answer_list)-1)]
        return random_answer

    composed_answer = list()
    for intent in assorted_intents[0]:
        answer_list = state_intents[intent]["answers"]
        random_answer = answer_list[random.randint(0, len(answer_list)-1)]
        composed_answer.append(random_answer)
    return '. '.join(composed_answer) or ""


def fallback_response(fallback) -> str:
    return fallback[random.randint(0, len(fallback)-1)]


def state_answer(flow, cState, user_reply):
    # names
    current_state: dict = flow[cState["state"]]
    state_intents = current_state["intents"]
    state_iterations = cState["intent_iterations"]
    fallback = current_state["fallback"]
    matched_intents = find_matches(state_intents, state_iterations, user_reply)

    # actions
    sort_intents_priority(matched_intents, current_state["intents"])
    assorted_intents: Tuple[list,list] = extract_overiterated(matched_intents, state_intents, state_iterations)
    print(annotated_intents(assorted_intents))
    final_answer: str = compose_answer(assorted_intents, state_intents)
    return final_answer or fallback_response(fallback)

def apiKey():
    if not "OPENAI_API_KEY" in os.environ:
        with open("config.json", "r") as c:
            config = json.load(c)
            os.environ["OPENAI_API_KEY"] = config["openai_api_key"]
