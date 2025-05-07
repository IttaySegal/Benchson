import os
import yaml
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ibm import WatsonxLLM
from config.model import model_name, model_parameters
from pathlib import Path
from langchain_core.prompts import PromptTemplate

class LLMJsonGenerator:

    def __init__(self):
        yaml_path = Path(__file__).parent / "prompts.yaml"
        with open(yaml_path, "r", encoding="utf-8") as f:
            self._cfg = yaml.safe_load(f)

        self.llm = WatsonxLLM(
            url=os.getenv("WATSONX_API_ENDPOINT"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            apikey=os.getenv("WATSONX_API_KEY"),
            model_id=model_name,
            params=model_parameters
        )

    def make_prompt(self, name: str) -> PromptTemplate:
        entry = self._cfg[name]
        return PromptTemplate(
            input_variables=entry["input_variables"],
            template=entry["template"]
        )

    def prompt_generator(self, parser, prompt_object):
        chain = self.make_prompt(prompt_object["name"]) | self.llm | parser()
        return chain.invoke(prompt_object["input_variables"])
