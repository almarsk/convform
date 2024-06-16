import re
import json

result = "V této větě jsou dvě podstatná jména: \"indie\" a \"žánry\". \n\n- \"indie\" zde pravděpodobně odkazuje na hudební žánr, což je abstraktní pojem, nikoli konkrétní entita.\n- \"žánry\" je také abstraktní pojem, který neodkazuje na konkrétní entitu.\n\nProtože ani jedno z těchto podstatných jmen nepředstavuje konkrétní entitu, výstup bude prázdný.\n\n```json\n[]\n```"

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
