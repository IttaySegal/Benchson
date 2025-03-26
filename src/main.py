import json
from validation import json_schema_validator, json_validator
from LLMJsonGenerator import LLMJsonGenerator

if __name__ == "__main__":
    print("Initializing LLMJsonGenerator...")
    generator = LLMJsonGenerator()

    structure = "Basic Item List"
    theme = "Cybersecurity"
    modification_type = "Add new key, and relevant values"

    print(f"\nTheme: {theme}")
    print(f"Structure: {structure}")
    print(f"Modification type: {modification_type}")

    print("\nGenerating JSON schema...")
    json_schema = generator.json_schema_generator(theme, structure)
    if not json_schema_validator(json_schema):
        print("json schema not valid")
        breakpoint()
    print("JSON Schema generated:")
    print(json.dumps(json_schema, indent=2))

    print("\nGenerating original JSON from schema...")
    origin_json = generator.json_generator(json_schema, 1)
    if not json_validator(origin_json,json_schema):
        print("json not valid")
        breakpoint()
    print("Original JSON generated:")
    print(json.dumps(origin_json, indent=2))

    print("\nModifying JSON based on instruction...")
    modified_json = generator.modified_json_generator(origin_json, modification_type)
    print("Modified JSON:")
    print(json.dumps(modified_json, indent=2))

    print("\nGenerating description of the modification...")
    description = generator.description_output_generator(origin_json, modified_json)
    print("Description of modification:")
    print(description)





# llm = WatsonxLLM(
#     url=os.getenv("WATSONX_API_ENDPOINT"),
#     project_id=os.getenv("WATSONX_PROJECT_ID"),
#     apikey=os.getenv("WATSONX_API_KEY"),
#     model_id=model_name,
#     params=model_parameters
# )
#
# json_prompt = PromptTemplate(
#     input_variables=["structure", "topic", "num_of_tokens"],
#     template="Can you create a JSON file for me in a {structure} structure on the topic of {topic}, Maximum length {num_of_tokens} tokens."
# )
# json_chain = json_prompt | llm | JsonOutputParser()
#
# structure = "Basic Item List" #get_random_structure()
# topic = "Cybersecurity" #get_random_theme()
# num_of_tokens = 50 #random.randint(30, 100)
#
# json_res = json_chain.invoke({
#     "structure": structure,
#     "topic": topic,
#     "num_of_tokens": num_of_tokens
# })
# print(f"structure: {structure}, topic: {topic}")
# print(f"JSON: {json_res}")
#
# modify_prompt = PromptTemplate(
#     input_variables=["json_data", "instruction", "num_of_tokens"],
#     template="Here is a JSON object:\n{json_data}\nPlease {instruction}, and return only the updated JSON object without any further explanation. Maximum length {num_of_tokens} tokens."
# )
# modify_chain = modify_prompt | llm | JsonOutputParser()
#
# modification = "Add new key, and relevant values" #get_random_modification()
#
# modified_res = modify_chain.invoke({
#     "json_data": json_res,
#     "instruction": modification,
#     "num_of_tokens": num_of_tokens+30
# })
# print(f"After Change: {modified_res}")
#
# explain_prompt = PromptTemplate(
#     input_variables=["before", "after"],
#     template="Here is the original JSON:\n{before}\nAnd here is the modified JSON:\n{after}\nWrite me in a few words the change you made."
# )
# explain_chain = explain_prompt | llm | StrOutputParser()
#
# explanation = explain_chain.invoke({
#     "before": json_res,
#     "after": modified_res
# })
# print(f"The modification I was asked to make is: {modification}. {explanation}")