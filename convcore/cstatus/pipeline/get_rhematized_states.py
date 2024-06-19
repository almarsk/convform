from os import setuid
import pprint
from sys import getswitchinterval

debug = False

def get_rhematized_states(flow, states, context_states, usage, coda, time_to_initiate, fallback_states):

    if debug:
        print("states", states)

    # order adjacents by index
    ordered_states = [
        state
        for [index, states]
        in sorted([
            [state["index"], state["adjacent"]]
            for _, state
            in states.items()
        ], key=lambda x: x[0])
        for state in states
    ]

    if debug:
        print("ordered states", ordered_states)

    ordered_states += [state for state in context_states if state not in ordered_states]

    if debug:
        print("os + context", ordered_states)

    get_full_state = lambda searched_state: [
        state
        for state in flow.states
        if state.name == searched_state
        ][0]

    # filter out overiterated states including connectives
    rhematized_states = list()
    previous_connective = ""
    initiatives = []

    # only use one initiative and append it at the end
    for state in ordered_states:
        if debug:
            print("candidate and current", state, rhematized_states)
        full_state = get_full_state(state)

        if debug:
            print("emph", state, full_state.emphasis)

        is_connective = full_state.response_type == "connective"
        if is_connective:
            previous_connective = full_state.name
            if debug:
                print("connective", state)
            continue

        if debug:
            print("usage",usage)
            print("iter", full_state.iteration)

        is_overiterated = full_state.iteration <= 0 or full_state.iteration - usage.get(state, 0) <= 0
        is_initiative = full_state.response_type == "initiative" or full_state.response_type == "flexible"

        if is_initiative and not is_overiterated:
            if debug:
                print("init non over iter", state)
            initiatives.append([previous_connective, state] if previous_connective else [state])
            continue

            if debug:
                print("is init and is over", is_initiative, is_overiterated)

        elif not is_initiative and not is_overiterated and state not in rhematized_states:
            print("responsive non over", state)

            if previous_connective:
                rhematized_states.append(previous_connective)
            rhematized_states.append(state)
        previous_connective = ""

    if debug:
        print("pre emph rhem", rhematized_states)

    emphasised = [state for state in rhematized_states if get_full_state(state).emphasis]

    if debug:
        print("emph", emphasised)

    if emphasised:
        return [emphasised[-1]]
    else:
        print("not emph")
        rhematized_states += (initiatives[-1] if initiatives else [])

    if debug:
        print("rhem + init", rhematized_states)


    if debug:
        print("rhem + emph", rhematized_states)

    if not initiatives and not coda and time_to_initiate:
        track_state = add_least_iterated_non_over_iterated(flow.track, flow, usage)
        if track_state:
            rhematized_states.append(track_state)

    if debug:
        print("rhem + track", rhematized_states)

    if not rhematized_states:
        # add fallback states
        rhematized_states += fallback_states

    if debug:
        print("rhem + fallback", rhematized_states)

    # this effectively sets coda to true, because states that are in coda will be found in last states
    if not rhematized_states:
        coda_state = add_least_iterated_non_over_iterated(flow.coda, flow, usage)
        if coda_state:
            rhematized_states.append(coda_state)

    if debug:
        print("coda", rhematized_states)

    return rhematized_states


def add_least_iterated_non_over_iterated(states, flow, usage):
    get_full_state = lambda searched_state: [
        s for s in flow.states if s.name == searched_state
        ][0]

    candidates = [state
            for state in states
            if get_full_state(state).iteration >= 0
            and get_full_state(state).iteration - usage.get(state, 0) > 0
    ]

    print("candidate",candidates)

    return candidates[0] if candidates else None
