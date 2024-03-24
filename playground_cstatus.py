from convproof import validate_flow
from convcore.cstatus.cstatus import ConversationStatus
from convcore import Flow
import pprint

from app import app

with app.app_context():

    cs = {
        "bot_turns": 1,
        "coda": False,
        "context_intents": [],
        "context_states": [],
        "end": False,
        "history_intents": [[]],
        "history_states": [["intro"]],
        "initiativity": 1,
        "last_states": ["intro"],
        "matched_intents": {},
        "possible_intents": {},
        "previous_last_states": [],
        "prompt_log": [],
        "prompted_say": "jé ahoj",
        "raw_say": [{"prompt": False, "text": "jé ahoj"}],
        "say": "jé ahoj",
        "state_usage": {"intro": 1},
        "turns_history": [{"say": "jé ahoj", "who": "bot"}],
        "turns_since_initiative": 1
    }


    flow_name = "test_resolve"
    flow = Flow(flow_name)

    user_speech = "nemám rád psy ale mám rád špagety"
    c = ConversationStatus(user_speech, flow, cs).__dict__

    pprint.pp(c)
