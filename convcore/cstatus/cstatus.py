import random
from typing import Dict
from typing_extensions import Any

from .pipeline.get_to_match import get_to_match
from .pipeline.get_matched_intents import get_matched_intents
from .pipeline.is_initiative import is_initiative
from .pipeline.get_current_initiativity import get_current_initiativity
from .pipeline.gather_context_states import gather_context_states
from .pipeline.gather_context_intents import gather_context_intents
from .pipeline.get_rhematized_states import get_rhematized_states
from convcore.prompting.utilz import  resolve_prompt

from concurrent.futures import ThreadPoolExecutor

HISTORY_LEN = 3

class ConversationStatus:
    bot_turns: int
    previous_last_states: Any
    possible_intents: Any
    prompt_log: Any
    matched_intents: Any
    last_states: list
    turns_since_initiative: int
    initiativity: int
    context_intents: list
    context_states: list
    history_intents: Any
    history_states: Any
    state_usage: dict[str, int]
    raw_say: Any
    prompted_say: Any
    say: Any
    end: Any
    coda: bool
    turns_history: Any

    def __init__(self, user_speech, flow, prev_cs, structure=False):

        # number of bot turns
        # increments at the end of __init__
        self.bot_turns = (
            0 if prev_cs is None
            else prev_cs["bot_turns"]
        ) + 1

        # move last states of previous cso to previous last states of current cso
        self.previous_last_states = (
            list() if prev_cs is None
            else prev_cs["last_states"]
        )
        # collect intents from now previous last states
        self.possible_intents = (
            {} if prev_cs is None
            else self.to_match(flow, prev_cs["context_intents"])
        )

        self.prompt_log = []

        # decide which intents have been matched
        self.matched_intents = self.match_intents(
            user_speech,
            flow,
            prev_cs["turns_history"]+[{"say": user_speech, "who": "human"}] if prev_cs is not None else [])

        # process adjacent states to have max one initiative etc
        self.last_states = [] if structure else ([flow.track[0]]
            if prev_cs is None
            else self.rhematize(
            flow,
            prev_cs["context_states"],
            prev_cs["state_usage"],
            prev_cs["coda"],
            prev_cs["initiativity"] - prev_cs["turns_since_initiative"] <= 0
            )
        )

        # mark down initiativity
        self.turns_since_initiative = self.update_turns_since_initiative(
            0 if prev_cs is None
            else prev_cs["turns_since_initiative"],
            flow)

        # update initiativity for next round
        self.initiativity = self.update_initiative(flow, prev_cs["initiativity"] if prev_cs else 1)

        # update context intents based on matched intents and last states
        self.context_intents = self.update_context_intents(
            list() if prev_cs is None
            else prev_cs["context_intents"],
            flow)

        # extract context states for next round
        self.context_states = self.get_context_states(flow)

        # update history
        self.history_intents = (
            [] if prev_cs is None
            else prev_cs["history_intents"]
        ) + [list(self.matched_intents.keys())]

        # update history
        self.history_states = (
            [] if prev_cs is None
            else prev_cs["history_states"]
        ) + [self.last_states]

        # update state usage
        self.state_usage = self.update_state_usage(
            flow,
            dict() if prev_cs is None
            else dict(prev_cs["state_usage"]),
            self.last_states, self.matched_intents.keys())

        # check if coda has started
        self.coda = self.check_for_coda(flow)

        # assemble reply
        self.raw_say = self.assemble_reply(flow)

        # replace prompt sections with llm output
        self.prompted_say = self.prompt_reply(
            prev_cs["turns_history"] + [{"say": user_speech, "who": "human"}]
            if prev_cs else [{"say": user_speech, "who": "human"}],
            flow.persona
        )
        # finalize answer via prompting
        self.say = self.finalize_reply()

        # if there is no reply, it is the end of convo
        self.end = self.raw_say is None or not self.raw_say

        self.turns_history = [
            {"say": self.say, "who": "bot"}] if prev_cs is None else prev_cs["turns_history"] + [
            {"say": user_speech, "who": "human"}
        ] + [
            {"say": self.say, "who": "bot"}
        ]

    #_______ pipeline _______

    def to_match(self, flow, prev_context_intents):
        return get_to_match(flow, self.previous_last_states, prev_context_intents)


    def add_to_prompt_log(self, addition):
        self.prompt_log += addition


    def match_intents(self, user_speech, flow, history):
        to_match_intent_names = dict(self.possible_intents)

        if not to_match_intent_names:
            return {}

        matched_intents_with_index = get_matched_intents(
            flow,
            to_match_intent_names.keys(),
            user_speech,
            (history[HISTORY_LEN*-1:]
                if len(history) >= HISTORY_LEN
                else history),
            self.add_to_prompt_log)

        #print("matched cstatus", matched_intents_with_index)
        #print("tomatch cstatus", to_match_intent_names)

        return {key: {
            "adjacent": value,
            "index": matched_intents_with_index[key]
        } for key, value in to_match_intent_names.items() if key in list(matched_intents_with_index.keys())}


    def rhematize(self, flow, context_states, usage, coda, time_to_initiate):
        return get_rhematized_states(
            flow,
            self.matched_intents,
            context_states,
            usage,
            coda,
            time_to_initiate
        )


    def update_turns_since_initiative(self, previous_number_of_turns, flow):
        return 0 if is_initiative(self.last_states, flow) else previous_number_of_turns + 1


    def update_initiative(self, flow, prev_value):
        return get_current_initiativity(self.last_states, flow, prev_value)


    def get_context_states(self, flow):
        return gather_context_states(self.last_states, flow)


    def update_context_intents(self, prev_context_intents, flow):
        return gather_context_intents(
            prev_context_intents,
            self.matched_intents.keys(),
            flow,
            self.last_states
        )

    def update_state_usage(self, flow, previous_state_usage, last_states, matched_intents):
        get_full_state = lambda state: [s for s in flow.states if s.name == state][0]
        get_full_intent = lambda intent: [i for i in flow.intents if i.name == intent][0]

        # including incrementing iteration from within states
        for state in last_states:
            if state not in previous_state_usage:
                previous_state_usage[state] = 0
            previous_state_usage[state] += 1

            for iterated in get_full_state(state).iterate_states:
                if iterated not in previous_state_usage:
                    previous_state_usage[iterated] = 0
                previous_state_usage[iterated] += 1
        for intent in matched_intents:
            for iterated in get_full_intent(intent).iterate_states:
                if iterated not in previous_state_usage:
                    previous_state_usage[iterated] = 0
                previous_state_usage[iterated] += 1

        return previous_state_usage


    def check_for_coda(self, flow):
        coda = flow.coda
        return bool([state for state in self.last_states if state in coda])


    def assemble_reply(self, flow):
        raw_says = []
        get_full_state = lambda state: [s for s in flow.states if s.name == state][0]
        for state in self.last_states:
            full_state = get_full_state(state)
            say_info = full_state.say[random.randint(0, len(full_state.say) - 1)]
            say_info["emphasis"] = full_state.emphasis
            raw_says.append(
                say_info
            )
        return raw_says


    def prompt_reply(self, history, persona):
        context = (history[HISTORY_LEN*-1:]
            if len(history) >= HISTORY_LEN
            else history)
        prompts = [{
            "persona": persona,
            "prompt": say["text"],
            "context": context if not say["emphasis"] else [],
            "log": self.add_to_prompt_log,
            "chain": say["prompt"]
        } for say in self.raw_say if say["prompt"]]

        with ThreadPoolExecutor() as exec:
            results = exec.map(resolve_prompt, prompts)
            exec.shutdown(wait=True)
            resolved = list(results)
        prompted = [say["text"] if not say["prompt"] else resolved.pop(0) for say in self.raw_say]
        return prompted

    def finalize_reply(self):
        # TODO check order and add missed info via global prompting
        return " ".join(self.prompted_say)
