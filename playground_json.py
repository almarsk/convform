import re
import json

result = "Věta \"nejradši v lehátku\" obsahuje jedno podstatné jméno \"lehátku\". Toto podstatné jméno představuje konkrétní věc, která může být považována za entitu, protože se jedná o fyzický objekt, který lze identifikovat a odkázat na něj.\n\nVýstup tedy bude:\n```json\n[\"lehátku\"]\n```"
print("r", result)
json_output = re.findall(str(r"\[.*\]"), result)

print(json_output)

print("j")
for j in json_output:
    print(j)
    print(json.loads(j))

entities = json.loads(json_output[-1])

print(["entities:"])
print([entities])

print(entities)
