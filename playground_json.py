import re
import json


result = "Jasně, odpověď by mohla vypadat třeba takhle: Viděli jste už nějaké velké vodopády na vlastní oči?"
result2 = "Viděli jste už nějaké velké vodopády na vlastní oči?"
split_on = "Jasně, odpověď by mohla vypadat třeba takhle:"
print(result)

print(result.split(split_on)[-1].strip())
print(result2.split(split_on)[-1].strip())
