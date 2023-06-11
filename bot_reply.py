from utils import *
import pprint


def reply(user_reply, cState):
    cState.setdefault("state", "state_start")
    cState.setdefault("global_turn", 0)
    cState.setdefault("intent_iterations", {})
    flow: dict = get_flow_json(cState["flow"])

    if cState["global_turn"] == 0:
        cState["global_turn"] += 1
        cState["state"] = "state_intro"
        return flow["state_start"]["greet"]
    else:
        current_state: dict = flow[cState["state"]]
        state_intents = current_state["intents"]
        state_iterations = cState["intent_iterations"]
        fallback = current_state["fallback"]
        matched_intents = find_matches(state_intents, state_iterations, user_reply)

        if len(matched_intents):
            sort_intents_priority(matched_intents, current_state["intents"])
            assorted_intents: Tuple[list,list] = extract_overiterated(matched_intents, state_intents, state_iterations)
            print(annotated_intents(assorted_intents))
            final_answer = get_answer(assorted_intents, state_intents)
            if final_answer:
                return final_answer
            else:
                return fallback_response(fallback)
        else:
            return fallback_response(fallback)

    # TODO
    #                           add intents to be able to test multi intent answer composition
    #                           compose answer based on matched intents, priority and over-iteration
    #                           edge-cases: all over-iterated   - over-iterated answer + steering the conversation
    #                                       no matches          - AI fallback management
    #                           come up with another state to be able to test steering the convo as a fallback
    #                           make sure the robot speech is loaded async, right now theres a hardcoded timeout
    #
    #
    #
    #
    #
    #______________________________________________________________________________________________________________
    # reactivity            -   see all the matched intents and compose an answer based on priority
    #                       -   leave the over-iterated ones out (if there are any un-overiterated)
    #                       -   in case of only overiterating steering the convo
    #
    # steering the convo    -   next possible state in case theres not iniciative to react to
    #                       -   have AI determine whether there is no iniciative to react to
    #                               - if there is no iniciative - easy going phrase/steering the convo
    #                       -   or whether there is an uncaught intent - automate suggesting edits to the flow JSON
    #
    # over-iteration behavior - next state? steering the convo?
    #
    # have AI manage            1) fallbacks 2) establishing topics (later, vec dbs)
    #                           fallback-   look for intent based on names of intents
    #                                   -   create an answer trying to steer the person back
    #                                       to general overview of convo defined in state_start (TODO)
    #


# TESTING SECTION
loc_test = False
if loc_test:
    cState0 = {
        "flow" : "zvědavobot",
    }
    cState1 = {
        "flow" : "zvědavobot",
        'global_turn': 2,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 0,
            'jak se máš': 0
        }
    }
    cState2 = {
        "flow" : "zvědavobot",
        'global_turn': 3,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 1,
            'jak se máš': 0
        }
    }
    cState3 = {
        "flow" : "zvědavobot",
        'global_turn': 3,
        'state': 'state_intro',
        'intent_iterations': {
            'pozdrav': 2,
            'jak se máš': 1
        }
    }

    print("bot: "+reply("", cState0))
    print("usr: "+"ahoj")
    print("bot: "+reply("ahoj", cState1))
    print("bot: "+reply("ahoj jak se máš", cState2))
    print("bot: "+reply("ahoj jak se máš", cState3))
