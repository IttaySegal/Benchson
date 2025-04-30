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
        "- The schema must include at least one property of each of the following types: `string`, `integer`, `float`, `boolean`, `array`, and `object`.\n"
        "- Each field must be explicitly defined using the `type` keyword."
        "- Include additional constraints like minLength, maximum, enum, minItems, maxItems, required only when applicable and relevant to the theme.\n"
        "- Include arrays with a valid `items` definition and objects with nested properties when applicable.\n"
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
            "You are an assistant specialized in generating JSON Schemas that conform to the JSON Schema Draft-07 specification.\n"
            "Your task is to create a strictly valid JSON Schema based on the following two input parameters:\n\n"
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
            "Output:"
        )
    )


def json_generator_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["schema", "number"],
        template=(
            "You are an assistant specialized in generating JSON data that conforms exactly to a given schema.\n\n"
            "You will receive two inputs:\n"
            "1. `{schema}` — A complete JSON Schema definition. This schema defines the structure, types, and constraints of valid JSON instances.\n"
            "2. `{number}` — The number of valid JSON instances you must generate.\n\n"
            "Your task is to generate exactly {number} JSON instances that strictly conform to the rules and constraints defined in the schema.\n"
            "Each instance must satisfy all of the following requirements:\n"
            "- All required fields must be present.\n"
            "- Field types must match those specified in the schema.\n"
            "- Any constraints such as `minLength`, `maxLength`, `minimum`, `maximum`, `enum`, `pattern`, `format`, `minItems`, and `maxItems` must be respected.\n\n"
            "Your response must follow this requirements:\n"
            "- You must output exactly {number} valid JSON instances.\n"
            "- Each instance must be a valid JSON string.\n"
            "- Do not include any explanations, comments, or markdown formatting.\n"
            "- Do not include any descriptive text — only the raw JSON instances.\n"
            "Output:"
        )
    )




def json_modification_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["schema", "json_instance", "instruction"],
        template=(
            "You are an assistant specialized in applying precise modifications to JSON objects while ensuring strict adherence to a provided schema.\n\n"
            "You will receive three inputs:\n"
            "1. `{schema}` — A complete JSON Schema definition. This schema defines the allowed structure, types, required fields, and constraints for valid JSON instances.\n"
            "2. `{json_instance}` — A valid JSON object that must remain valid according to the schema after the modification is applied.\n"
            "3. `{instruction}` — A specific, unambiguous instruction describing exactly one modification to apply to the JSON.\n\n"
            "Your task is to modify the JSON instance according to the instruction while following these strict requirements:\n"
            "- The modified JSON must continue to fully comply with the provided schema.\n"
            "- You must not introduce any changes that would violate field types, required fields, value constraints (such as `minLength`, `maximum`, `enum`, `pattern`, etc.), or structural rules defined in the schema.\n"
            "- If applying the instruction would cause the JSON to become invalid under the schema, you must return the original JSON instance unchanged.\n"
            "- You must preserve the overall structure and constraints of the original JSON wherever possible.\n"
            "Your response must follow this requirements:\n"
            "- Always use double quotes (`\"`) for all keys and string values — never use single quotes.\n"
            "- The output must be valid JSON only — do not include any markdown syntax (e.g., ```json), comments, or any explanatory text.\n"
            "- The output must be a single valid JSON string and nothing else.\n"
            "Your response must be deterministic: applying the instruction should result in exactly one correct modified JSON instance.\n\n"
            "Output:"
        )
    )


def input_modification_generator_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["schema", "original_json", "modification_type"],
        template=(
            "You are an assistant specialized in generating precise and executable user instructions for modifying JSON objects.\n\n"
            "You will receive three inputs:\n"
            "1. `{schema}` — A complete JSON Schema definition, specifying the valid structure, types, required fields, and constraints for the JSON object.\n"
            "2. `{original_json}` — The original JSON object before any modification. This is provided for context only; you must not reference or mention it in your output.\n"
            "3. `{modification_type}` — A description of the type of modification the user wants to make (e.g., change a value, remove a key, append to an array).\n\n"
            "Your task is to generate a single, clear, natural-language instruction that a user might say to request the specified modification.\n\n"
            "The instruction must follow this requirements:\n"
            "- The instruction must be specific enough so that applying it would produce exactly one modified version of the JSON object.\n"
            "- The instruction must describe exactly one change that can be directly and immediately applied to the original JSON object.\n"
            "- The change must be fully legal and valid according to the provided JSON Schema (respect field types, allowed values, required fields, and constraints).\n"
            "- The instruction must make sense in the context of the original JSON structure and content.\n"
            "Your response must follow this requirements:\n"
            "- Do not include any quotation marks, markdown formatting, or explanatory text.\n"
            "- Do not reference or mention the original JSON explicitly (e.g., do not say 'in the JSON above').\n"
            "- The instruction must describe a single, atomic change — no multi-step instructions.\n\n"
            "Your goal is to produce a single instruction that could immediately be executed by an assistant to apply one precise and schema-valid change to the JSON.\n\n"
            "Output:"
        )
    )


def description_output_modification_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["before", "after"],
        template=(
            "You are a JSON modification explainer. Your task is to analyze two versions of a JSON object: "
            "You will receive two inputs:\n"
            "1. `{before}` — the original version of the JSON object.\n"
            "2. `{after}` — the modified version of the JSON object.\n\n"
            "Both inputs will be provided as raw JSON strings.\n\n"
            "Your task is to carefully compare the two versions and generate a single, concise sentence that accurately describes the modification that was made.\n"
            "You must focus precisely on what was added, removed, or changed.\n\n"
            "Your response must follow this requirements:\n"
            "- The description must be **specific and detailed**, clearly mentioning what field or value was modified.\n"
            "- The description must not be general or vague — it must describe exactly what changed.\n"
            "- If there is no difference between the two versions, output exactly: 'No modification was made.'\n"
            "- Output only the description sentence, with no extra formatting, preambles, or commentary.\n\n"
            "- Do not include any quotation marks, markdown formatting, or explanatory text.\n"
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

