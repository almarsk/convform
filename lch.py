from langchain.prompts import PromptTemplate
from langchain import OpenAI, LLMChain
import os
from utils import api_key

async def fill_in(persona, task):
    api_key()
    template = "Tvoje osobnost: {p} Tvůj úkol: {t} Tvá další odpověď:"
    prompt_template = PromptTemplate.from_template(template)
    prompt = PromptTemplate(template=template, input_variables=["p", "t"])
    chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0.8))



    return chain.run(p=persona, t=task)
