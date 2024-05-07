import convcore.prompting.chains.intent.entity as e
from convcore.prompting.utilz import api_key

import json
import codecs

api_key()
q = e.entity({
    "speech": "Přišel jsem si pro ty švestky k vám",
    "name": "bruh"
}, bench=True)

print(q)
