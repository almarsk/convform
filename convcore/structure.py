from convcore import State, Intent, Flow
from convcore.cstatus import ConversationStatus
import re

def structure():
    state_anno = {key: get_quoted_value_or_full_string(value) for key, value in State.__annotations__.items()}
    intent_anno = { key: get_quoted_value_or_full_string(value) for key, value in Intent.__annotations__.items()}
    flow_anno = {key: get_quoted_value_or_full_string(value) for key, value in Flow.__annotations__.items() if key != "states" and key != "intents"}
    cstatus_anno = { key: get_quoted_value_or_full_string(value) for key, value in ConversationStatus.__annotations__.items()}


    states_ordered = [[key, state_anno[key]] for key in list(State({}).__dict__.keys()) if key in state_anno]
    intent_ordered = [[key, intent_anno[key]] for key in list(Intent({}).__dict__.keys()) if key in intent_anno]
    flow_ordered = [[key, flow_anno[key]] for key in list(Flow("", structure=True).__dict__.keys()) if key in flow_anno]
    cstatus_ordered = [[key, cstatus_anno[key]] for key in list(ConversationStatus("", Flow("", structure=True), None, structure=True).__dict__.keys()) if key in cstatus_anno]

    return states_ordered, intent_ordered, flow_ordered, cstatus_ordered

def get_quoted_value_or_full_string(value):
    match = re.search(r"'([^']*)'", str(value))
    if match:
        return match.group(1)
    else:
        return str(value)
