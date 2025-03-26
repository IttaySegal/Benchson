from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM
import os
import random
from config.model import model_name, model_parameters
from utils import get_random_structure, get_random_theme,  get_random_modification

llm = WatsonxLLM(
    url=os.getenv("WATSONX_API_ENDPOINT"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    apikey=os.getenv("WATSONX_API_KEY"),
    model_id=model_name,
    params=model_parameters
)

json_prompt = PromptTemplate(
    input_variables=["structure", "topic", "num_of_tokens"],
    template="Can you create a JSON file for me in a {structure} structure on the topic of {topic}, Maximum length {num_of_tokens} tokens."
)
json_chain = json_prompt | llm | JsonOutputParser()

structure = get_random_structure()
topic = get_random_theme()
num_of_tokens = random.randint(30, 100)

json_res = json_chain.invoke({
    "structure": structure,
    "topic": topic,
    "num_of_tokens": num_of_tokens
})
print(f"structure: {structure}, topic: {topic}")
print(f"JSON: {json_res}")

modify_prompt = PromptTemplate(
    input_variables=["json_data", "instruction", "num_of_tokens"],
    template="Here is a JSON object:\n{json_data}\nPlease {instruction}, and return only the updated JSON object without any further explanation. Maximum length {num_of_tokens} tokens."
)
modify_chain = modify_prompt | llm | JsonOutputParser()

modification = get_random_modification()

modified_res = modify_chain.invoke({
    "json_data": json_res,
    "instruction": modification,
    "num_of_tokens": num_of_tokens+30
})
print(f"After Change: {modified_res}")

explain_prompt = PromptTemplate(
    input_variables=["before", "after"],
    template="Here is the original JSON:\n{before}\nAnd here is the modified JSON:\n{after}\nWrite me in a few words the change you made."
)
explain_chain = explain_prompt | llm | StrOutputParser()

explanation = explain_chain.invoke({
    "before": json_res,
    "after": modified_res
})
print(f"The modification I was asked to make is: {modification}. {explanation}")