from registered_chains import registered_chains

def proof_chain(bot, issues):
    for state in bot["states"]:
        for say in state["say"]:
            if say["prompt"] and say["prompt"] not in registered_chains["state"]:
                issues.append(f"prompt {say['prompt']} in {state['name']} missing")

    for intent in bot["intents"]:
        for match in intent["match_against"]:
            if match["prompt"] and match["prompt"] not in registered_chains["intent"]:
                issues.append(f"prompt {match['prompt']} in {intent['name']} missing")
