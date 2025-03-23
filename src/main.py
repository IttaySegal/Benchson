from langchain_core.output_parsers import StrOutputParser
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

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(
    input_variables=["adjective"], template=prompt_template
)
chain = prompt | llm | StrOutputParser()

res = chain.invoke({"adjective": "dogs"})
print(res)