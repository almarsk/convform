import pprint

def proof_empty(bot, issues):
    try:
        for key, value in bot.items():
            if not value:
                issues.append(f"{key} empty")

        for state in bot["states"]:
            if not state["say"]:
                issues.append(f"say in state {state['name']} empty")

            for intent, adjacent in state["intents"].items():
                if adjacent or default_adjacent(intent, bot):
                    pass
                else:
                    issues.append(f"intent {intent} in state {state['name']} empty")

        for intent in bot["intents"]:
            if not intent["match_against"]:
                issues.append(f"match_against in intent {intent['name']} empty")

        context_intents = [(context_intent, intent["name"], "intent")
            for intent in bot["intents"]
            for context_intent in intent["context_intents"]
        ] + [(context_intent, state["name"], "state")
            for state in bot["states"]
            for context_intent in state["context_intents"]]

        for context_intent_name, source_item_name, source_item_type in context_intents:
            adjacent = [intent for intent in bot["intents"]][0]["adjacent"]
            if not adjacent:
                issues.append(f"context intent {context_intent_name} in {source_item_type} {source_item_name} empty")





    except Exception as e:
        issues.append(e)

def default_adjacent(intent, bot):
    try:
        is_adjacent = len([i for i in bot["intents"] if i["name"] == intent][0]["adjacent"]) > 0
        return is_adjacent
    except:
        return False
