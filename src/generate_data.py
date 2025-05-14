import json
import os
import re
from validation import json_schema_validator, json_validator
from LLM_json_generator import LLMJsonGenerator
from json_comparator import compare_json_object
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


def generate_data(counter, theme, structure, modifications_path,base_folder, schema_type):
    generator = LLMJsonGenerator()
    print(theme, structure)

    # Read modification types from file
    with open(modifications_path, 'r', encoding='utf-8') as f:
        modifications = [line.strip() for line in f if line.strip()]

    # Output folders
    names = ['data', 'errors', 'no_changes', 'schemas', 'diffs']
    folders = {n: os.path.join(base_folder, n) for n in names}
    for path in folders.values():
        os.makedirs(path, exist_ok=True)


    # Generate JSON schema
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
        return counter

    print("✅ JSON Schema generated.")

    # Save schema file
    name = re.split(r'[^a-zA-Z0-9]', structure.strip())[0]
    schema_file_name = f"schema_{theme}_{name}.json"
    schema_file_path = os.path.join(folders['schemas'], schema_file_name)
    with open(schema_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(json_schema, out_file, indent=2)

    # Loop over modifications
    for mod in modifications:
        # Generate original JSON
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

            # Special case for “Remove duplicate elements…”:
            # Since the original JSON instance may not actually contain any duplicates to remove,
            # we first inject duplicates by applying an “Add duplicate elements to an array” modification.
            # That gives us a new JSON (with guaranteed duplicates), which we then feed into the normal
            # “Remove duplicate elements” instruction below.
            if mod == "Remove duplicate elements from an array: Identify and eliminate repeated elements within an array to ensure uniqueness.":
                instruction = generator.prompt_generator(StrOutputParser, {
                    "name": "input_instruction",
                    "input_variables": {
                        "schema": json_schema,
                        "original_json": origin_json,
                        "modification_type": "Add duplicate elements to an array: Insert one or more values that are already present in the array to create duplicates."
                    }
                })
                origin_json = generator.prompt_generator(JsonOutputParser,{
                    "name": "modify_json",
                    "input_variables": {
                        "schema": json_schema,
                        "json_instance": origin_json,
                        "instruction": instruction
                    }
                })
            # Generate the actual instruction for the requested modification (including the cleaned-up
            # “Remove duplicate elements…” case above) and apply it
            instruction = generator.prompt_generator(StrOutputParser, {
                "name": "input_instruction",
                "input_variables": {
                    "schema": json_schema,
                    "original_json": origin_json,
                    "modification_type": mod
                }
            })
            modified_json = generator.prompt_generator(JsonOutputParser,{
                    "name": "modify_json",
                    "input_variables": {
                        "schema": json_schema,
                        "json_instance": origin_json,
                        "instruction": instruction
                    }
                })

            # Validate modified JSON
            if not json_validator(modified_json, json_schema):
                print(f"❌ Modified JSON is INVALID against schema for modification: {mod}")
                save_error_case(counter, {
                    "origin_json": origin_json,
                    "instruction": instruction,
                    "modified_json": modified_json
                }, json_schema, mod, folders['errors'], error_type="modified_invalid")
                counter += 1
                continue

            # Create the JSON structure for evaluation
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

            # Compare using eval_data
            is_equal = compare_json_object(eval_data, diffs_folder=folders['diffs'], instance_id=str(counter))

            # Decide folder based on whether a real change occurred
            if is_equal:
                target_folder = folders['no_changes']
                print(f"🟰 No change detected for {mod}, saving in no-change folder.")
            else:
                target_folder = folders['data']
                print(f"✅ Change detected for {mod} saving in instances folder.")

            # Write the evaluation data to a JSON file
            file_name = f"instance_{counter}.json"
            file_path = os.path.join(target_folder, file_name)
            with open(file_path, 'w', encoding='utf-8') as out_file:
                json.dump(eval_data, out_file, indent=2)

            counter += 1

    return counter

def save_error_case(counter, error_data, json_schema, modification_type, error_folder, error_type="error"):
    """
    Save error JSONs separately for analysis.
    """
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
