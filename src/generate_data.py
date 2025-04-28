import json
from validation import json_schema_validator, json_validator
from LLMJsonGenerator import LLMJsonGenerator
import os

# Global Counter for numbering files
counter = 1

def generate_valid_data(theme, structure, modifications_path, output_folder, error_folder):
    global counter
    generator = LLMJsonGenerator()
    print(theme, structure)

    # Read modification types from file
    with open(modifications_path, 'r', encoding='utf-8') as f:
        modifications = [line.strip() for line in f if line.strip()]

    # Generate JSON schema
    json_schema = generator.strict_json_schema_generator(theme, structure)
    if not json_schema_validator(json_schema):
        print("❌ JSON schema not valid.")
        return

    print("✅ JSON Schema generated.")

    # Ensure output and error folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)

    # Loop over modifications
    for modification_type in modifications:
        # Generate original JSON
        origin_json = generator.json_generator(json_schema, 1)

        if not json_validator(origin_json, json_schema):
            print(f"❌ Original JSON not valid against schema for modification: {modification_type}")
            save_error_case(origin_json, modification_type, error_folder, error_type="origin_invalid")
            continue

        # Special case handling
        if modification_type == "Remove duplicate elements from an array: Identify and eliminate repeated elements within an array to ensure uniqueness.":
            instruction = generator.input_generator(json_schema, origin_json, "Add duplicate elements to an array: Insert one or more values that are already present in the array to create duplicates.")
            origin_json = generator.modified_json_generator(json_schema, origin_json, instruction)

        instruction = generator.input_generator(json_schema, origin_json, modification_type)
        modified_json = generator.modified_json_generator(json_schema, origin_json, instruction)

        # Validate modified JSON
        if not json_validator(modified_json, json_schema):
            print(f"❌ Modified JSON is INVALID against schema for modification: {modification_type}")
            save_error_case({
                "origin_json": origin_json,
                "instruction": instruction,
                "modified_json": modified_json
            }, modification_type, error_folder, error_type="modified_invalid")
            continue

        # Create the JSON structure for evaluation
        eval_data = {
            "data": origin_json,
            "instructions": instruction,
            "ground_truth": modified_json,
            "modification": generator.description_output_generator(origin_json, modified_json)
        }

        # Write the evaluation data to a JSON file
        file_name = f"instance_{counter}.json"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as out_file:
            json.dump(eval_data, out_file, indent=2)

        print(f"✅ Successfully created: {file_path}")
        counter += 1  # Increment the global counter after each file is created


def save_error_case(error_data, modification_type, error_folder, error_type="error"):
    """
    Save error JSONs separately for analysis.
    """
    global counter
    error_filename = f"error_{error_type}_{counter}.json"
    error_path = os.path.join(error_folder, error_filename)

    error_record = {
        "modification_type": modification_type,
        "error_type": error_type,
        "error_data": error_data
    }

    with open(error_path, 'w', encoding='utf-8') as error_file:
        json.dump(error_record, error_file, indent=2)

    print(f"⚠️  Saved error case: {error_path}")
    counter += 1
