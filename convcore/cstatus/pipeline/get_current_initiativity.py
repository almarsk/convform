def get_current_initiativity(last_states, flow):



    initiativy_values = [
        state.initiativity
        for state in flow.states
        if state.name in last_states
        and state.initiativity >= 0
    ]

    # max or min? 💀
    return min(initiativy_values) if initiativy_values else 1
