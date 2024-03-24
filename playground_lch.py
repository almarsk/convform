from convcore.prompting.playground.func_call_intent_reco_index import test_func_call
from convcore.prompting.playground.correction_order import correction_order
from convcore.prompting.playground.resolve_para import resolve_para

prompts = [
    #["vypráví o morčatech jak jsou hebká", False],
    #["vypráví o morčatech jak jsou hebká", True],
    ["odpoví na otázku", True],
    ["neodpoví na otázku", True],
]
for r in resolve_para(prompts):
    print(r+"\n")
