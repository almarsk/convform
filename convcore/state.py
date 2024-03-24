from enum import Enum
from .say import Say

class ResponseType(Enum):
    INITIATIVE = 'initiative'
    RESPONSIVE = 'responsive'
    FLEXIBLE = 'flexible'
    CONNECTIVE = 'connective'

class State:
    name: str
    intents: dict
    say: list[tuple[Say,str]]
    response_type: ResponseType
    emphasis: bool
    iteration: int
    initiativity: int
    context_intents: list
    context_states: list
    iterate_states: list
    def __init__(self, state):
        self.name = state.get("name", "")
        self.intents = state.get("intents", {})
        self.say = state.get("say", [])
        self.response_type = state.get("response_type", ResponseType.RESPONSIVE)
        self.emphasis = state.get("emphasis", False)
        self.iteration = state.get("iteration", 1)
        self.initiativity = state.get("initiativity", 1)
        self.context_intents = state.get("context_intents", [])
        self.context_states = state.get("context_states", [])
        self.iterate_states = state.get("iterate_states", [])
