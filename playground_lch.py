import convcore.prompting.playground.anafora as e
from convcore.prompting.utilz import api_key

import json
import codecs

api_key()
q = e.an2fora({}, bench=True)

print(q)
