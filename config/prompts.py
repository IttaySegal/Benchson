from langchain_core.prompts import PromptTemplate


def schema_system_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""You are an assistant designed to generate JSON schemas based on given story structures and themes."""
    )

# def strict_valid_schema_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Generate a valid JSON Schema that conforms to the JSON Schema Draft-07 standard. The schema must meet the following requirements:
#
#         1. Specify the `$schema` field as "http://json-schema.org/draft-07/schema#" to define the version.
#         2. Use valid keywords such as `type`, `properties`, `required`, and `items` to define object and array structures.
#         3. All fields must be explicitly defined with their correct data types using the `type` keyword.
#         4. Apply constraints such as `minLength`, `maximum`, `enum`, `format`, or others only when appropriate.
#         5. Use `"additionalProperties": false` to ensure that no extra key-value pairs are allowed beyond those explicitly defined.
#         6. Do not include any fields or structures that are not explicitly described in the provided structure.
#         7. The schema must enforce strict typing: types must not be changed or left ambiguous.
#
#         Generate only the JSON Schema as output."""
#     )

# def valid_schema_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Generate a valid JSON Schema. The schema must conform to the JSON Schema Draft-07 standard and include the following elements:
#         1. Specify the `$schema` field as "http://json-schema.org/draft-07/schema#" to define the version.
#         2. Use valid properties such as `type`, `properties`, `required`, and `items` for objects and arrays.
#         3. Ensure all fields are properly defined with their types, and use constraints like `minLength`, `maximum`, or `enum` only when applicable."""
#     )

def strict_json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""Generate a valid JSON Schema about {theme} with the following structure format: {structure}
        - The schema must conform to the JSON Schema Draft-07 standard.
        - The schema should include between 20 and 40 fields, ensuring a diverse range of types, including:
          - `string`, `integer`, `number`, `boolean`, `array`, `dictionary` and `object`.
        - All fields must be explicitly defined with correct types using the `type` keyword.
        - Ensure at least one field of each type (`string`, `integer`, `number`, `boolean`, `array`, `object`) is present.
        - Do not change the type of any value from the original structure if specified.
        - Use constraints like `minLength`, `maximum`, `enum`, `minItems`, `maxItems`, or `required` only when applicable.
        - Include arrays with a valid `items` definition and objects with nested properties when relevant.
        - Disallow any properties not explicitly defined by setting `"additionalProperties": false` in all object definitions.
        - Specify the `$schema` field as "http://json-schema.org/draft-07/schema#".
        Your response must contain only the JSON Schema. Do not include any explanations, descriptions, or additional text.
        Return the schema as a string.""",
        input_variables=["theme", "structure"]
    )

def json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""Generate a valid JSON Schema about {theme} with the following structure format: {structure}
        - The schema should be valid.
        - The schema should include 20-40 fields.
        - Ensure all fields are properly defined with their types.
        - Include constraints like `minLength`, `maximum`, or `enum` only when applicable.
        - Specify the `$schema` field as "http://json-schema.org/draft-07/schema#" to define the version.
        Your response must contain only the JSON Schema. Do not include any descriptions, explanations, or additional text.
        Return the schema as a string.""",
        input_variables=["theme", "structure"]
    )

def simple_json_schema() -> PromptTemplate:
    return PromptTemplate(
        template="""{
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer", "minimum": 0 },
        "email": { "type": "string", "format": "email" }
      },
      "required": ["name", "age"]
    }"""
    )

def json_generator_system_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""You are an AI designed to generate long and complex JSON instances based on a provided JSON schema. 
        The schema defines the structure, types, and constraints for JSON objects. 
        Always ensure the generated JSON is strictly valid according to the schema."""
    )

def json_generator_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""Using the following schema
        {schema}
        Create the {number} valid JSON instance that strictly adheres to the schema's rules, including constraints like required fields, field types, and specified formats.
        Ensure the JSON instance is varied but fully compliant with the schema.
        Your response must contain only the JSON. Do not include any descriptions, explanations, or additional text.""",
        input_variables=["schema", "number"]
    )

def json_modification_system_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""You are an assistant tasked with receiving a valid JSON instance and applying a deliberate modification based on the provided instruction.
        Your task is to update the JSON instance while preserving the overall structure unless the instruction requires significant changes.
        Always ensure the updated output is strictly valid JSON using double quotes for keys and strings."""
    )

# def json_modification_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Using the following valid JSON instance {json_instance}, please apply the following modification: {instruction}.
#         Return only the updated valid JSON instance. Do not include any descriptions, explanations, or additional text.""",
#         input_variables=["json_instance", "instruction"]
#     )

def json_modification_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""Using the following valid JSON instance: {json_instance}
        Apply the following modification: {instruction}
        Return only the updated *valid JSON*.
        - Ensure all keys and string values are enclosed in double quotes.
        - Do NOT return Python-style output (e.g., single quotes or capitalized keys).
        - Do NOT wrap the output in markdown (e.g., ```json).
        - Do NOT include any explanations or comments — return the JSON instance only.
        - If the requested modification cannot be applied to the provided JSON instance (e.g., attempting to append to a non-existent array), return the original JSON instance unchanged.""",
    input_variables=["json_instance", "instruction"]
    )

def input_modification_generator_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""You are simulating a user giving an instruction to modify a JSON object.
        original JSON (for reference only, do not include in output):
        {original_json}
        Desired modification: {modification_type}
        Write a direct instruction from the user to an assistant that clearly describes the modification they want to make.
        Only output the instruction, without any explanation or formatting.""",
        input_variables=["original_json", "modification_type"]
    )

def description_output_modification_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""You are an assistant that explains the modifications made to a JSON file.
        Given the following original JSON:
        {before}
        And the modified JSON:
        {after}
        Provide a brief description of the modifications made to the JSON.
        The response must follow this format:
        Description of Modification: <One sentence describing what was changed>""",
        input_variables=["before", "after"]
    )
