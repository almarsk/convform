def get_current_initiativity(last_states, flow, prev_value):


    initiativy_values = [
        state.initiativity
        for state in flow.states
        if state.name in last_states
        and state.initiativity >= 0
    ]

    print("init",initiativy_values)
    print("prev",prev_value)

    # max or min? 💀
    return min(initiativy_values) if initiativy_values else prev_value
