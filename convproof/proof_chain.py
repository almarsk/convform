from registered_chains import registered_chains

def proof_chain(bot, issues):
    for state in bot["states"]:
        for say in state["say"]:
            if say["prompt"] and say["prompt"] not in registered_chains:
                issues.append(f"prompt {say['prompt']} in {state['name']} missing")
