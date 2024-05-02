def get_current_initiativity(last_states, flow, prev_value):


    initiativy_values = [
        state.initiativity
        for state in flow.states
        if state.name in last_states
        and state.initiativity >= 0
    ]


    return min(initiativy_values) if initiativy_values else prev_value
