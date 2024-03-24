import json

nula = {'function_call': {'arguments': '{"variants":["a) prozradil co d\\\\u011bl\\\\u00e1","b) zeptal se jak se m\\\\u00e1","c) post\\\\u0119\\\\u017eoval si na po\\\\u010das\\\\u00ed","d) pochv\\\\u00e1lil po\\\\u010das\\\\u00ed","e) nic z nab\\\\u00eddnut\\\\u00fdch mo\\\\u017enost\\\\u00ed"]}', 'name': 'choose_variants'}}

jedna = str({'function_call': {'arguments': '{"variants":["a) prozradil co d\\u011bl\\u00e1","b) zeptal se jak se m\\u00e1","c) post\\u0119\\u017eoval si na po\\u010das\\u00ed","d) pochv\\u00e1lil po\\u010das\\u00ed","e) nic z nab\\u00eddnut\\u00fdch mo\\u017enost\\u00ed"]}', 'name': 'choose_variants'}})

dva = str({'function_call': {'arguments': '{"variants":["a) prozradil co d\u011bl\u00e1","b) zeptal se jak se m\u00e1","c) post\u0119\u017eoval si na po\u010das\u00ed","d) pochv\u00e1lil po\u010das\u00ed","e) nic z nab\u00eddnut\u00fdch mo\u017enost\u00ed"]}', 'name': 'choose_variants'}})

tři = bytes(dva, "utf-8").decode("unicode_escape")

print(tři)
