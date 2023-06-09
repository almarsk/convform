import json
import random
import re


def reply(user_reply, cState):
    cState.setdefault("state", "state_intro")
    cState.setdefault("global_turn", 0)
    cState.setdefault("intent_iterations", {})
    print(cState)

    if cState["global_turn"] == 0:
        cState["global_turn"] += 1
        return "brejdn"
    else:
        with open("flows/klomp.json", "r") as k:
            flow = json.load(k)
            current_state = flow[cState["state"]]

            for intent in current_state["intents"]:
                current_intent = current_state["intents"][intent]

                for item in current_intent["keywords"]:
                    if re.search(item, user_reply):
                        answers = current_state["intents"][intent]["answer"]
                        cState["intent_iterations"].setdefault(intent, 0)
                        cState["intent_iterations"][intent] += 1

                        if cState["intent_iterations"][intent] <= current_intent["iteration"]:
                            return answers[random.randint(0, len(answers)-1)] # throw in a pool of possibilities
                        elif cState["intent_iterations"][intent] > current_intent["iteration"]:
                            over_iterated_answers = current_intent["over_iterated_answers"]
                            return over_iterated_answers[random.randint(0, len(over_iterated_answers)-1)]

            fallback = current_state["fallback"]
            return fallback[random.randint(0, len(fallback)-1)]


        # fallbacks missing
        # error handling - loading json, reading json
        # regex
        # instead of returning answer directly, throw in a pool and compare priorities

        # changing states
loc_test = False
if loc_test:

    cState = {
        "global_turn":1
        }

    print(reply("čawík", cState))
    print(reply("nazdárek", cState))
    print(reply("jak se máš ty darebo", cState))
