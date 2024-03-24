from .say import Say

class Intent:
    name: str
    match_against: list[tuple[Say,str]]
    adjacent: list
    context_intents: list
    iterate_states: list

    def __init__(self, intent):
        self.name = intent.get("name", "")
        self.match_against = intent.get("match_against", [])
        self.adjacent = intent.get("adjacent", [])
        self.context_intents = intent.get("context_intents", [])
        self.iterate_states = intent.get("iterate_states", [])
