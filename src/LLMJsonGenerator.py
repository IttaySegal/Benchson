from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ibm import WatsonxLLM
from config.model import model_name, model_parameters
import os
import config.prompts as prompts


class LLMJsonGenerator:
    def __init__(self):
        self.llm = WatsonxLLM(
            url=os.getenv("WATSONX_API_ENDPOINT"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            apikey=os.getenv("WATSONX_API_KEY"),
            model_id=model_name,
            params=model_parameters
        )

    def json_schema_generator(self, theme, structure):
        prompt = prompts.json_schema_human_prompt()
        chain = prompt | self.llm | JsonOutputParser()
        json_schema = chain.invoke({
            "theme": theme,
            "structure": structure
        })
        return json_schema

    def json_generator(self, json_schema, json_num):
        chain = prompts.json_generator_human_prompt() | self.llm | JsonOutputParser()
        json = chain.invoke({
            "schema": json_schema,
            "number": json_num
        })
        return json

    def modified_json_generator(self, original_json, modification_type):
        chain = prompts.json_modification_human_prompt() | self.llm | JsonOutputParser()
        modified_json = chain.invoke({
            "json_instance": original_json,
            "instruction": modification_type #self.input_generator(original_json, modification_type)
        })
        return modified_json

    def input_generator(self, original_json, modification_type):
        chain = prompts.input_modification_generator_prompt() | self.llm | StrOutputParser()
        input_prompt = chain.invoke({})
        return input_prompt

    def description_output_generator(self, original_json, modified_json):
        chain = prompts.description_output_modification_prompt() | self.llm | StrOutputParser()
        description_output = chain.invoke({
            "before": original_json,
            "after": modified_json
        })
        return description_output
