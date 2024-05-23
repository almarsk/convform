from .say import Say

class Intent:
    name: str
    match_against: list[tuple[Say,str]]
    adjacent: list
    iteration: int
    context_intents: list
    iterate_states: list
    checkpoint: bool

    def __init__(self, intent):
        self.name = intent.get("name", "")
        self.match_against = intent.get("match_against", [])
        self.adjacent = intent.get("adjacent", [])
        self.iteration = intent.get("iteration", 1)
        self.context_intents = intent.get("context_intents", [])
        self.iterate_states = intent.get("iterate_states", [])
        self.checkpoint = intent.get("checkpoint", False)
