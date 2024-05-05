matched_intents = {
    "lol": {
        "adjacent": []
    },
}


intents = {
    "lol": ["bruh"]
}


for matched_intent in matched_intents:
    if matched_intent in intents.keys():
        matched_intents[matched_intent]["adjacent"] += intents[matched_intent]

print(matched_intents)
