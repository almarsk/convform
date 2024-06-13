def get_current_initiativity(last_states, matched_intents, flow, prev_value):


    initiativy_values = [
        state.initiativity
        for state in flow.states
        if state.name in last_states
        and state.initiativity >= 0
    ] + [
        intent.initiativity
        for intent in flow.intents
        if intent.name in matched_intents
        and intent.initiativity >= 0
        and hasattr(intent, 'initiativity')
    ]

    return min(initiativy_values) if initiativy_values else prev_value
