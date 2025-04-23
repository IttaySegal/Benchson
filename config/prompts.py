from langchain_core.prompts import PromptTemplate


def strict_json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["theme", "structure"],
        template=
        "You are an assistant specialized in generating JSON Schemas that conform to the JSON Schema Draft-07 specification.\n"
        "Your task is to create a strictly valid JSON Schema based on the following two input parameters:\n"
        "1. `{theme}` — This describes the high-level subject or domain the schema should represent.\n"
        "2. `{structure}` — This describes the general layout or conceptual organization of the schema.\n\n"
        "Based on these inputs, you must generate a JSON Schema that:\n"
        "- Clearly represents the theme through semantically appropriate and logically named properties.\n"
        "- Strictly conforms to the JSON Schema Draft-07 standard.\n"
        "- The schema must include between 20 and 40 properties in total.\n"
        "- The schema must include at least one property of each of the following types: `string`, `integer`, `float`, `number`, `boolean`, `array`, and `object`.\n"
        "- Uses the type keyword for all fields, and includes additional constraints (minLength, maximum, enum, minItems, maxItems, required) only when relevant to the theme.\n"
        "- Defines the items schema for all arrays and includes nested properties for all objects where applicable.\n"
        "- Sets `additionalProperties: false` on all object definitions to restrict extra fields.\n"
        "- Specifies the $schema field as http://json-schema.org/draft-07/schema#.\n\n"
        "Your response must include:\n"
        "- Only the JSON Schema as a valid JSON string.\n"
        "- No markdown formatting, no explanations, and no extra text — just the schema.\n"
        "Output:"
    )


def dynamic_json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["theme", "structure"],
        template=(
            "You are an assistant specialized in generating JSON Schemas that conform to the JSON Schema Draft-07 specification. Your task is to create a strictly valid JSON Schema based on the following two input parameters:\n\n"
            "You will receive two inputs:\n"
            "1. `{theme}` — This describes the high-level subject or domain the schema should represent.\n"
            "2. `{structure}` — This describes the general layout or conceptual organization of the schema.\n\n"
            "Your task is to create a single JSON Schema that matches the provided theme and structure while adhering to the following strict requirements:\n"
            "- The schema must be valid according to the JSON Schema Draft-07 specification.\n"
            "- Include at least 20 fields across the schema, using a variety of types: `string`, `integer`, `number`, `boolean`, `array`, and `object`.\n"
            "- Include at least one conditional block using `if`, `then`, and `else` keywords to add dynamic behavior.\n"
            "- Use nested objects and arrays with properly defined `properties` and `items` where appropriate.\n"
            "- Specify required fields using the `required` keyword to enforce validation rules.\n"
            "- Include at least one example of conditional logic, such as:\n"
            "  • If a specific field has a given value, then require additional fields.\n"
            "  • If a condition is met, the type or structure of another field must change.\n"
            "- Set `additionalProperties: true` at relevant levels to allow for flexible extensions.\n"
            "- Include the `$schema` declaration as: `\"$schema\": \"http://json-schema.org/draft-07/schema#\"` at the top level.\n\n"
            "Your response must follow this requirements:\n"
            "- Output only the JSON Schema as a valid JSON string.\n"
            "- Do not include any explanations, comments, examples, or markdown formatting.\n"
            "- The output must be fully deterministic and syntactically correct.\n\n"
            "Output:"
        )
    )


def json_generator_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["schema", "number"],
        template=(
            "You are an assistant specialized in generating JSON data that conforms exactly to a given schema.\n\n"
            "You will be provided with two inputs:\n"
            "1. `{schema}` — A complete JSON Schema definition. This schema defines the structure, types, and constraints of valid JSON instances.\n"
            "2. `{number}` — The number of valid JSON instances you must generate.\n\n"
            "Your task is to generate exactly {number} JSON instances that strictly conform to the rules and constraints defined in the schema. "
            "Each instance must satisfy all of the following where applicable:\n"
            "- All required fields must be present.\n"
            "- Field types must match those specified in the schema.\n"
            "- Any constraints such as `minLength`, `maxLength`, `minimum`, `maximum`, `enum`, `pattern`, `format`, `minItems`, and `maxItems` must be respected.\n\n"
            "Your response must follow this requirements:\n"
            "- You must output exactly {number} valid JSON instances.\n"
            "- Each instance must be a valid JSON string.\n"
            "- Do not include any explanations, comments, or markdown formatting.\n"
            "- Do not include any descriptive text — only the raw JSON instances.\n"
            "- Each output must be deterministic and reproducible given the same schema.\n\n"
            "Output:"
        )
    )


def json_modification_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["json_instance", "instruction"],
        template=(
            "You are an assistant specialized in applies precise modifications to JSON objects.\n\n"
            "You will receive two inputs:\n"
            "1. `{json_instance}` — This is a valid JSON object that must remain valid after the modification is applied.\n"
            "2. `{instruction}` — This is a specific, unambiguous instruction written in natural language, describing exactly one modification to apply to the JSON.\n\n"
            "Your task is to produce a new JSON object that reflects exactly the modification described in the instruction. The output must be a valid JSON object, "
            "You must follow these strict requirements:\n"
            "- Preserve the overall structure and constraints of the original JSON where applicable.\n"
            "- Always use double quotes (`\"`) for all keys and all string values — never use single quotes.\n"
            "- Output must be valid JSON only — do not include any markdown syntax (e.g., ` ```json `), comments, or extra text.\n"
            "- The output must be a single JSON string and nothing else.\n"
            "- If the instruction refers to a key or structure that does not exist (e.g., appending to a missing array), you must return the original JSON unchanged.\n\n"
            "Your response must be deterministic: applying the instruction should produce one and only one correct modified JSON.\n\n"
            "Output:"
        )
    )


def input_modification_generator_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["original_json", "modification_type"],
        template=(
            "You are an assistant specialized in generating a precise and unambiguous instruction that a user might give to modify a JSON object.\n\n"
            "You will receive two inputs:\n"
            "1. `{original_json}` — This is the original JSON object before any modifications. You must use this only for reference to understand the context. "
            "You must not include any part of it in your final output.\n"
            "2. `{modification_type}` — This describes the kind of modification the user wants to make, such as changing a value, removing a key, or appending to an array.\n\n"
            "Your task is to generate a single, clear instruction that a user would naturally say when requesting this specific type of change. "
            "The instruction must be detailed and specific enough that exactly one modified version of the JSON object could be produced by applying the change. "
            "There should be no ambiguity or multiple possible interpretations.\n\n"
            "Your response must follow this requirements:\n"
            "- Output only the instruction, phrased as a direct user request.\n"
            "- The instruction must describe one and only one specific modification.\n"
            "- Do not include any quotes, markdown formatting, explanations, or multiple steps.\n"
            "- Do not reference the original JSON explicitly (e.g., don’t say 'In the JSON above...').\n\n"
            "Your goal is to output a single line that could be read by an assistant and immediately turned into one exact change to the original JSON.\n\n"
            "Output:"
        )
    )


def description_output_modification_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["before", "after"],
        template=(
            "You are a JSON modification explainer. Your task is to analyze two versions of a JSON object: "
            "`{before}`, which represents the original version, and `{after}`, which represents the modified version. "
            "These two inputs will be provided as raw JSON. Your job is to determine what changed between them and output "
            "a single, concise sentence describing the modification. Focus on what was added, removed, or changed.\n\n"
            "Your output must follow these rules:\n"
            "- If there is no difference between the two versions, output: 'No modification was made.'\n"
            "- Output only the description sentence, with no extra formatting, preambles, or commentary.\n\n"
            "Output:"
        )
    )


# def schema_system_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""You are an assistant designed to generate JSON schemas based on given story structures and themes."""
#     )

# def json_schema_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Generate a valid JSON Schema about {theme} with the following structure format: {structure}
#         - The schema should be valid.
#         - The schema should include 20-40 fields.
#         - Ensure all fields are properly defined with their types.
#         - Include constraints like `minLength`, `maximum`, or `enum` only when applicable.
#         - Specify the `$schema` field as "http://json-schema.org/draft-07/schema#" to define the version.
#         Your response must contain only the JSON Schema. Do not include any descriptions, explanations, or additional text.
#         Return the schema as a string.""",
#         input_variables=["theme", "structure"]
#     )

# def valid_schema_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Generate a valid JSON Schema. The schema must conform to the JSON Schema Draft-07 standard and include the following elements:
#         1. Specify the `$schema` field as "http://json-schema.org/draft-07/schema#" to define the version.
#         2. Use valid properties such as `type`, `properties`, `required`, and `items` for objects and arrays.
#         3. Ensure all fields are properly defined with their types, and use constraints like `minLength`, `maximum`, or `enum` only when applicable."""
#     )

# def simple_json_schema() -> PromptTemplate:
#     return PromptTemplate(
#         template="""{
#       "$schema": "http://json-schema.org/draft-07/schema#",
#       "type": "object",
#       "properties": {
#         "name": { "type": "string" },
#         "age": { "type": "integer", "minimum": 0 },
#         "email": { "type": "string", "format": "email" }
#       },
#       "required": ["name", "age"]
#     }"""
#     )

# def json_generator_system_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""You are an AI designed to generate long and complex JSON instances based on a provided JSON schema.
#         The schema defines the structure, types, and constraints for JSON objects.
#         Always ensure the generated JSON is strictly valid according to the schema."""
#     )

# def json_modification_system_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""You are an assistant tasked with receiving a valid JSON instance and applying a deliberate modification based on the provided instruction.
#         Your task is to update the JSON instance while preserving the overall structure unless the instruction requires significant changes.
#         Always ensure the updated output is strictly valid JSON using double quotes for keys and strings."""
#     )

# def json_modification_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""Using the following valid JSON instance {json_instance}, please apply the following modification: {instruction}.
#         Return only the updated valid JSON instance. Do not include any descriptions, explanations, or additional text.""",
#         input_variables=["json_instance", "instruction"]
#     )

