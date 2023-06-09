import json
import random
import re


def reply(user_reply, cState):
    cState.setdefault("state", "state_intro")
    cState.setdefault("global_turn", 0)
    cState.setdefault("intent_iterations", {})

    if cState["global_turn"] == 0:
        cState["global_turn"] += 1
        return "brejdn"
    else:
        try:
            with open("flows/klomp.json", "r") as k:
                    flow = json.load(k)
        except FileNotFoundError:
            print("File not found")
            return "ajaj, ta moje hlava děravá, jsem nějaký rozbitý"
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            return "ajaj, nějak nevím, co jsem to chtěl říct, jsem nějaký rozbitý"
        except Exception as e:
            print("An error occurred:", str(e))
            return "ajaj něco se nepovedlo, jsem nějaký rozbitý"

        current_state = flow[cState["state"]]
        matched_intents = []

        for intent in current_state["intents"]:
            current_intent = current_state["intents"][intent]

            for item in current_intent["keywords"]:
                if re.search(item.lower(), user_reply.lower()):
                    cState["intent_iterations"].setdefault(intent, 0)
                    print(cState)
                    matched_intents.append(intent)


        # sorting intents by priority
        if len(matched_intents):
            matched_intents.sort(key=lambda intent: current_state["intents"][intent]["priority"], reverse=True)
            print("matched intents after sorting: ",matched_intents)
            iterating_intents = []

            # over-iterated intents are taken out of the list
            for possible_intent in matched_intents:
                current_possible_intent = current_state["intents"][possible_intent]
                if cState["intent_iterations"][possible_intent] > current_possible_intent["iteration"]:
                    print("iteration alert")
                    iterating_intents.append(matched_intents.pop(matched_intents.index(possible_intent)))

            # over-iterated intents are moved to the end of the list
            if len(iterating_intents):
                for intent in iterating_intents:
                    matched_intents.append(intent)
            print("matched intents after shifting iterated ones: ",matched_intents)

            # returning a random realization of the chosen intent answer
            if len(matched_intents):
                final_picked_intent = matched_intents[0]
                final_picked_answer_list = current_state["intents"][final_picked_intent]["answer"]
                return final_picked_answer_list[random.randint(0, len(final_picked_answer_list)-1)]

        # if there are no matches
        else:
            fallback = current_state["fallback"]
            return fallback[random.randint(0, len(fallback)-1)]



    # changing states
    # actual ai and such

# TESTING SECTION
loc_test = True
if loc_test:
    cState = {
        'global_turn': 1,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 2,
            'jak se máš': 0
        }
    }
    print(reply("čawík, jak je", cState))
