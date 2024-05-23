def proof_references(bot, issues):

    existing_states = [state["name"] for state in bot.get("states", []) if "name" in state]
    existing_intents = [intent["name"] for intent in bot.get("intents", []) if "name" in intent]

    state_refs = dict()
    intent_refs = dict()

    try:
        for state in bot["track"]:
            add_or_append(state, state_refs, "track")
        for state in bot["coda"]:
            add_or_append(state, state_refs, "coda")

        for state in bot["states"]:
            for substate in state["iterate_states"]:
                add_or_append(substate, state_refs, f"iterate_states of {substate} in {state['name']}")
            for substate in state["context_states"]:
                add_or_append(substate, state_refs, f"context states of {substate} in {state['name']}")
            if "context_intents" in state:
                for intent in state["context_intents"]:
                    add_or_append(intent, intent_refs, f"context intents of {intent} in {state['name']}")
            if "fallback_states" in state:
                for substate in state["fallback_states"]:
                    add_or_append(substate, state_refs, f"fallback states of {substate} in {state['name']}")
            for intent, adjacent in state["intents"].items():
                add_or_append(intent, intent_refs, f"intents in state {state['name']}")
                for substate in adjacent:
                    add_or_append(substate, state_refs, f"adjacent {substate} of intent {intent} in state {state['name']}")

        for intent in bot ["intents"]:
            for substate in intent["iterate_states"]:
                add_or_append(substate, state_refs, f"iterate states of {substate} in {intent['name']}")
            for subintent in intent["context_intents"]:
                add_or_append(subintent, intent_refs, f"context intents of {subintent} in {intent['name']}")
            for state in intent["adjacent"]:
                add_or_append(state, state_refs, f"adjacent in {intent['name']}")

    except Exception as e:
        issues.append(e)

    missing = dict()

    for state, location in state_refs.items():
        if state not in existing_states:
            missing[state] = ["state", ",".join(location)]
    for intent, location in intent_refs.items():
        if intent not in existing_intents:
            missing[intent] = ["intent", ",".join(location)]

    for missing_item, [type, location] in missing.items():
        issues.append(f"missing {type} {missing_item} found in {location}")

def add_or_append(key, my_dict, value):
    if key in my_dict:
        my_dict[key].append(value)
    else:
        my_dict[key] = [value]
