import json
import os
import re
from validation import json_schema_validator, json_validator
from LLM_json_generator import LLMJsonGenerator
from json_comparator import compare_json_object
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# 🧩 Mapping of modifications to their inverse setup injections
pre_mod_injection_map = {
    # 1. Remove Duplicates → Add Duplicates first
    "Remove duplicate elements from an array: Identify and eliminate repeated elements within an array to ensure uniqueness.": [
        "Add duplicate elements to an array: Insert one or more values that are already present in the array to create duplicates."
    ],

    # 2. Capitalization → First distort casing
    "Capitalize or format string values: Modify the format of a string, such as changing case uppercase/lowercase.": [
        "De-capitalize or randomly change case of string values: Make strings lowercase or mix cAsE to simulate formatting issues."
    ],

    # 3. Sort → Add elements to break order, then reverse
    "Sort array elements: Arrange elements within an array in a specific order, such as alphabetical, numerical, or custom-defined.": [
        "Append new elements to an array: Insert new random values at the end of one or more arrays.",
        "Reverse array elements: Flip the order of items in one or more arrays to make them reversed."
    ],

    # 4. Reverse → Add elements to break order, then sort
    "Reverse array elements: Rearrange elements in an array so that their order is flipped from end to start.": [
        "Append new elements to an array: Insert new random values at the end of one or more arrays.",
        "Sort array elements: Arrange the array elements in a clear ascending or alphabetical order."
    ]
}



def generate_data(counter, theme, structure, modifications_path, base_folder, schema_type):
    generator = LLMJsonGenerator()
    print(theme, structure)

    modifications = read_modifications(modifications_path)
    folders = setup_output_folders(base_folder)

    json_schema = generate_json_schema(generator, theme, structure, schema_type, folders['schemas'])
    if json_schema is None:
        return counter

    for mod in modifications:
        counter = process_modification(generator, json_schema, mod, folders, counter)

    return counter


def read_modifications(modifications_path):
    with open(modifications_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def setup_output_folders(base_folder):
    names = ['data', 'errors', 'no_changes', 'schemas', 'diffs']
    folders = {n: os.path.join(base_folder, n) for n in names}
    for path in folders.values():
        os.makedirs(path, exist_ok=True)
    return folders


def generate_json_schema(generator, theme, structure, schema_type, schema_folder):
    json_schema = generator.prompt_generator(JsonOutputParser, {
        "name": f"{schema_type}_json_schema",
        "input_variables": {
            "theme": theme,
            "structure": structure
        }
    })

    valid, error = json_schema_validator(json_schema)
    if not valid:
        print(f"❌ JSON schema not valid: {error}")
        return None

    print("✅ JSON Schema generated.")

    name = re.split(r'[^a-zA-Z0-9]', structure.strip())[0]
    schema_file_name = f"schema_{theme}_{name}.json"
    schema_file_path = os.path.join(schema_folder, schema_file_name)
    with open(schema_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(json_schema, out_file, indent=2)

    return json_schema


def generate_instruction(generator, schema, original_json, modification_type):
    return generator.prompt_generator(StrOutputParser, {
        "name": "input_instruction",
        "input_variables": {
            "schema": schema,
            "original_json": original_json,
            "modification_type": modification_type
        }
    })


def apply_modification(generator, schema, json_instance, instruction):
    return generator.prompt_generator(JsonOutputParser, {
        "name": "modify_json",
        "input_variables": {
            "schema": schema,
            "json_instance": json_instance,
            "instruction": instruction
        }
    })


def process_modification(generator, json_schema, mod, folders, counter):
    json_instances = generator.prompt_generator(JsonOutputParser, {
        "name": "json_instance",
        "input_variables": {
            "schema": json_schema,
            "number": 1
        }
    })

    for origin_json in json_instances:

        if not json_validator(origin_json, json_schema):
            print(f"❌ Original JSON not valid against schema for modification: {mod}")
            save_error_case(counter, {"origin_json": origin_json},
                            json_schema, mod, folders['errors'], error_type="origin_invalid")
            counter += 1
            continue

        # Apply precondition injection if defined
        if mod in pre_mod_injection_map:
            pre_mod_type = pre_mod_injection_map[mod]
            print(f"🔁 Pre-injection for '{mod}' using inverse instruction: '{pre_mod_type}'")

            instruction = generate_instruction(generator, json_schema, origin_json, pre_mod_type)
            origin_json = apply_modification(generator, json_schema, origin_json, instruction)

        # Generate instruction for requested modification
        instruction = generate_instruction(generator, json_schema, origin_json, mod)
        modified_json = apply_modification(generator, json_schema, origin_json, instruction)

        if not json_validator(modified_json, json_schema):
            print(f"❌ Modified JSON is INVALID against schema for modification: {mod}")
            save_error_case(counter, {
                "origin_json": origin_json,
                "instruction": instruction,
                "modified_json": modified_json
            }, json_schema, mod, folders['errors'], error_type="modified_invalid")
            counter += 1
            continue

        eval_data = {
            "data": origin_json,
            "instructions": instruction,
            "ground_truth": modified_json,
            "modification": generator.prompt_generator(StrOutputParser, {
                "name": "description",
                "input_variables": {
                    "before": origin_json,
                    "after": modified_json
                }
            })
        }

        is_equal = compare_json_object(
            eval_data,
            diffs_folder=folders['diffs'],
            instance_id=str(counter),
            modification_type=mod
        )

        if is_equal:
            target_folder = folders['no_changes']
            print(f"🟰 No change detected for {mod} saving in no-change folder.")
        else:
            target_folder = folders['data']
            print(f"✅ Change detected for {mod} saving in instances folder.")

        file_name = f"instance_{counter}.json"
        file_path = os.path.join(target_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as out_file:
            json.dump(eval_data, out_file, indent=2)

        counter += 1

    return counter


def save_error_case(counter, error_data, json_schema, modification_type, error_folder, error_type="error"):
    error_filename = f"error_{error_type}_{counter}.json"
    error_path = os.path.join(error_folder, error_filename)

    error_record = {
        "schema": json_schema,
        "modification_type": modification_type,
        "error_type": error_type,
        "error_data": error_data
    }

    with open(error_path, 'w', encoding='utf-8') as error_file:
        json.dump(error_record, error_file, indent=2)

    print(f"⚠️  Saved error case: {error_path}")
