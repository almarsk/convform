import pprint

def get_to_match(flow, last_states, context_intents):
    possible_intents = dict()
    flow_intents = flow.intents
    get_full_intent = lambda intent: [i for i in flow.intents if i.name == intent][0]

    for state in last_states:
        # find intents of state
        full_state = [s for s in flow.states if s.name == state][0]

        for intent, adjacent in full_state.intents.items():
            full_intent = get_full_intent(intent)
            if intent in possible_intents:
                possible_intents[intent] |= set(adjacent)
            else:
                possible_intents[intent] = set(full_intent.adjacent + adjacent)

    for intent in context_intents:
        full_intent = get_full_intent(intent)
        if intent in possible_intents:
            possible_intents[intent] |= set(full_intent.adjacent)
        else:
            possible_intents[intent] = set(full_intent.adjacent)


    return {key:list(value) for key, value in possible_intents.items()}
