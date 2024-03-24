def is_initiative(states, flow):
    # check in flow if at least one state is initiative

    initiative = [
        state.name for state
        in flow.states
        if state.name in states
        and state.response_type == "initiative"
    ]

    return bool(initiative)
