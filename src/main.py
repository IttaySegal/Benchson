from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM
import os
from config.model import model_name, model_parameters

llm = WatsonxLLM(
    url=os.getenv("WATSONX_API_ENDPOINT"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    apikey=os.getenv("WATSONX_API_KEY"),
    model_id=model_name,
    params=model_parameters
)

json_prompt = PromptTemplate(
    input_variables=["structure", "topic"],
    template="Can you create a JSON file for me in a {structure} structure on the topic of {topic}?"
)
json_chain = json_prompt | llm | JsonOutputParser()

json_res = json_chain.invoke({"structure": "music", "topic": "education"})
print(f"JSON: {json_res}")

modify_prompt = PromptTemplate(
    input_variables=["json_data", "instruction"],
    template="Here is a JSON object:\n{json_data}\nPlease {instruction}, and return only the updated JSON object"
)
modify_chain = modify_prompt | llm | StrOutputParser()

modified_res = modify_chain.invoke({
    "json_data": json_res,
    "instruction": "add new key-value pair"
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
print(f"Change: {explanation}")