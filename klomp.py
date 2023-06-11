from utils import *
import random
import re
import pprint


def reply(user_reply, cState):
    cState.setdefault("state", "state_start")
    cState.setdefault("global_turn", 0)
    cState.setdefault("intent_iterations", {})
    flow: dict = get_flow_json("klomp")

    if cState["global_turn"] == 0:
        cState["global_turn"] += 1
        cState["state"] = "state_intro"
        return flow["state_start"]["greet"]
    else:
        current_state: dict = flow[cState["state"]]
        state_intents = current_state["intents"]
        state_iterations = cState["intent_iterations"]
        fallback = current_state["fallback"]

        matched_intents = []
        for intent in state_intents:
            current_intent = state_intents[intent]

            for item in current_intent["keywords"]:
                if re.search(item.lower(), user_reply.lower()):
                    state_iterations.setdefault(intent, 0)
                    state_iterations[intent] += 1
                    matched_intents.append(intent)

        if len(matched_intents):
            sort_intents_priority(matched_intents, current_state["intents"])
            print(cState)
            final_answer = get_answer(extract_overiterated(matched_intents, state_intents, state_iterations), state_intents)
            if final_answer:
                return final_answer
            else:
                return fallback_response(fallback)
        else:
            return fallback_response(fallback)

    # steering the convo
    # changing states
    # actual ai and such

# TESTING SECTION
loc_test = True
if loc_test:
    cState = {
        'global_turn': 1,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 1,
            'jak se máš': 0
        }
        }
    print("bot: "+reply("", {}))
    print("usr: "+"ahoj")
    print("bot: "+reply("ahoj", cState))
