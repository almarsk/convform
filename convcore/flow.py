import json
import os
from convproof import validate_flow
from .state import State
from .intent import Intent

class Flow:
    track: list
    coda: list
    states: list
    intents: list
    def __init__(self, flow_name, structure=False):
        if not structure:
            flow = validate_flow( flow_name, return_flow=True)
        else:
            flow = {}
        self.track = flow.get("track", [])
        self.coda = flow.get("coda", [])
        self.states = [State(state) for state in flow.get("states", [])]
        self.intents = [Intent(intent) for intent in flow.get("intents", [])]
