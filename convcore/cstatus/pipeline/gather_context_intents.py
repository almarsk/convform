def gather_context_intents(prev_context_intents, matched_intents, flow, last_states):
    # remove matched ones
    removed_matched = [
        intent
        for intent in prev_context_intents
        if intent not in matched_intents
    ]
    # add context intents of matched intents
    context_intents_of_matched_intents = [
        item
        for intent in flow.intents
        if intent.name in matched_intents
        for item in intent.context_intents
    ]

    # add context intents of last states
    try:
        context_intents_of_last_states = [
            item
            for state in flow.states
            if state.name in matched_intents
            for item in state.context_intents
        ]
    except:
        print("issue getting context intents from last states")
        context_intents_of_last_states = []

    return removed_matched + context_intents_of_matched_intents + context_intents_of_last_states
