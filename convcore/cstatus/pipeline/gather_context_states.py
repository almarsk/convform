def gather_context_states(last_states, flow):
    context_states_unreduced = [
        state.context_states
        for state in flow.states
        if state.name in last_states
    ]

    context_states = [
        state
        for sublist in context_states_unreduced
        for state in sublist
    ]

    return context_states
