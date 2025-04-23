from langchain_core.prompts import PromptTemplate


# def strict_json_schema_human_prompt() -> PromptTemplate:
#     return PromptTemplate(
#         template="""
#         Generate a strictly valid JSON Schema based on the specified theme and structure.
#
#         Theme: {theme}
#         Structure: {structure}
#
#         Requirements:
#         - The schema must be directly relevant to the given theme. Ensure the schema's properties, naming conventions, and structure are logically connected to the theme.
#         - Adhere to the JSON Schema Draft-07 standard.
#         - Include between 20 and 40 fields, with a diverse range of types:
#           - `string`, `integer`, `number`, `boolean`, `array`, `object`.
#         - Each field must be explicitly defined using the `type` keyword.
#         - Ensure at least one field of each type (`string`, `integer`, `number`, `boolean`, `array`, `object`) is present.
#         - Do not alter the type of any value specified in the original structure.
#         - Use constraints like `minLength`, `maximum`, `enum`, `minItems`, `maxItems`, or `required` only when applicable and relevant to the theme.
#         - Include arrays with a valid `items` definition and objects with nested properties when applicable.
#         - Restrict objects to only defined properties by setting `"additionalProperties": false` for all object definitions.
#         - Specify the `$schema` field as `"http://json-schema.org/draft-07/schema#"`.
#
#         Important: Ensure that the schema represents a **valid JSON format directly related to the theme**.
#         For example, if the theme is "Learning Algorithms", the schema should include fields relevant to algorithms, such as `algorithm_name`, `complexity`, `implementation_language`, `author`, `description`, etc.
#
#         Output:
#         - Only return the JSON Schema as a valid JSON string.
#         - Do not include any explanations, descriptions, or additional text.
#         """,
#         input_variables=["theme", "structure"]
#     )

def strict_json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""
You are an assistant specialized in generating JSON Schemas that conform to the JSON Schema Draft-07 specification. Your task is to create a strictly valid JSON Schema based on the following two input parameters:

- Theme: {theme}
- Structure: {structure}

The **theme** represents the subject matter the schema should model. The **structure** defines the layout or format of the data.

Based on these inputs, you must generate a JSON Schema that:

- Clearly represents the theme through semantically appropriate and logically named properties.
- Strictly conforms to the JSON Schema Draft-07 standard.
- Includes **between 20 and 40 fields** of various types: `string`, `integer`, `number`, `boolean`, `array`, and `object`.
- Contains **at least one field** of each of the six types mentioned above.
- Uses the `type` keyword for all fields, and includes additional constraints (`minLength`, `maximum`, `enum`, `minItems`, `maxItems`, `required`) only when relevant to the theme.
- Defines the `items` schema for all arrays and includes nested `properties` for all objects where applicable.
- Sets `"additionalProperties": false` on all object definitions to restrict extra fields.
- Specifies the `$schema` field as `"http://json-schema.org/draft-07/schema#"`.

Your response must include:
- Only the JSON Schema as a valid JSON string.
- No markdown formatting, no explanations, and no extra text — just the schema.
""",
        input_variables=["theme", "structure"]
    )


def dynamic_json_schema_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""
        Generate a dynamic JSON Schema based on the provided theme and structure.

        Theme: {theme}
        Structure: {structure}

        Requirements:
        - The schema must comply with the JSON Schema Draft-07 standard.
        - Include at least 20 fields with a diverse range of types: `string`, `integer`, `number`, `boolean`, `array`, `object`.
        - Include at least **one conditional block** using the `if`, `then`, `else` keywords.
        - Allow for **additional keys** beyond the specified structure by setting `"additionalProperties": true` where applicable.
        - Include arrays with a valid `items` definition and objects with nested properties where relevant.
        - Ensure proper use of the `required` keyword to specify necessary fields.
        - Include conditional logic such as:
          - If a specific key is present and has a particular value, then additional keys must be required.
          - If a particular condition is met, the type of certain fields should change.
        - Specify the `$schema` field as `"http://json-schema.org/draft-07/schema#"`.

        Output:
        - Return only the JSON Schema as a valid JSON string.
        - Do not include any explanations, descriptions, or additional text.

        Example (simplified for demonstration purposes):
        If the theme is "Products", and the structure is "Product Catalog with categories and reviews":
        - If a product's `category` is `"electronics"`, then the `warranty_period` field is required.
        - If a product's `category` is `"food"`, then the `expiration_date` field is required.
        - Allow additional keys to be added for future product attributes.
        """,
        input_variables=["theme", "structure"]
    )


def json_generator_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""
        Using the provided schema:
        {schema}

        Generate {number} valid JSON instances that strictly adhere to the schema's rules and constraints, including:
        - Required fields, field types, and specified formats.
        - Constraints such as `minLength`, `maximum`, `enum`, `minItems`, `maxItems`, and `required` where applicable.

        Output:
        - Provide only the JSON instances as valid JSON strings.
        - Do not include any explanations, descriptions, or additional text.
        """,
        input_variables=["schema", "number"]
    )


def json_modification_human_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="""
        Given the following valid JSON instance: {json_instance}

        Apply the specified modification: {instruction}

        Requirements:
        - Maintain JSON validity and adhere to all original constraints where applicable.
        - Use only double quotes for all keys and string values.
        - Avoid Python-style output (e.g., single quotes or capitalized keys).
        - Do NOT wrap the output in markdown (e.g., ```json).
        - Do NOT include any explanations, comments, or additional text.
        - If the modification cannot be applied (e.g., appending to a non-existent array), return the original JSON instance unchanged.

        Output:
        - Only return the modified JSON instance as a valid JSON string.
        """,
        input_variables=["json_instance", "instruction"]
    )


def input_modification_generator_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["original_json", "modification_type"],
        template=(
            "You are simulating a user providing a natural-language instruction to modify a JSON object.\n\n"
            "Original JSON (for reference only, do not include it in the output):\n{original_json}\n\n"
            "Desired Modification Type:\n{modification_type}\n\n"
            "Task:\n"
            "- Write a clear, direct instruction from a user to an assistant that describes the desired modification.\n"
            "- The instruction should sound like a natural user request (e.g., 'Set the price to 29.99').\n"
            "- Do not include quotation marks around the instruction.\n"
            "- Do not include any explanation, justification, or formatting — only the raw instruction.\n\n"
            "Output:"
        )
    )


def description_output_modification_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["before", "after"],
        template=(
            "You are an assistant that describes changes made to a JSON object.\n\n"
            "Original JSON:\n{before}\n\n"
            "Modified JSON:\n{after}\n\n"
            "Task:\n"
            "- Provide a concise, one-sentence description of the modifications.\n"
            "- Focus on what was added, removed, or changed.\n"
            "- If no modification was made, state: 'No modification was made.'\n"
            "- Do not include extra formatting or explanation.\n\n"
            "Output: "
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

