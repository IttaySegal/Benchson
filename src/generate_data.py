import json
from validation import json_schema_validator, json_validator
from LLMJsonGenerator import LLMJsonGenerator
from json_comparator import compare_json_file
import os

# Global Counter for numbering files
counter = 1

def generate_valid_data(theme, structure, modifications_path, output_folder):
    global counter
    generator = LLMJsonGenerator()
    print(theme, structure)

    # Read modification types from file
    with open(modifications_path, 'r', encoding='utf-8') as f:
        modifications = [line.strip() for line in f if line.strip()]

    # Prepare output subfolders
    instances_folder = os.path.join(output_folder, "instances")
    diffs_folder = os.path.join(output_folder, "diffs")
    os.makedirs(instances_folder, exist_ok=True)
    os.makedirs(diffs_folder, exist_ok=True)

    # Generate JSON schema
    json_schema = generator.strict_json_schema_generator(theme, structure)
    if not json_schema_validator(json_schema):
        print("❌ JSON schema not valid.")
        return

    print("✅ JSON Schema generated.")

    # Save schema file
    schema_file_name = f"schema_{(counter + 17)//17}.json"
    schema_file_path = os.path.join(instances_folder, schema_file_name)
    with open(schema_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(json_schema, out_file, indent=2)

    # Loop over modifications
    for modification_type in modifications:
        # Generate original JSON
        origin_json = generator.json_generator(json_schema, 1)
        if not json_validator(origin_json, json_schema):
            print(f"❌ Original JSON not valid against schema for modification: {modification_type}")
            continue

        # Modify JSON
        instruction = generator.input_generator(origin_json, modification_type)
        modified_json = generator.modified_json_generator(origin_json, instruction)

        # Validate modified JSON
        if not json_validator(modified_json, json_schema):
            print(f"❌ Modified JSON is INVALID against schema for modification: {modification_type}")
            continue

        # Create the JSON structure for evaluation
        eval_data = {
            "data": origin_json,
            "instructions": instruction,
            "ground_truth": modified_json,
            "modification": generator.description_output_generator(origin_json, modified_json)
        }

        # Save evaluation instance to instances folder
        instance_file_name = f"instance_{counter}.json"
        instance_file_path = os.path.join(instances_folder, instance_file_name)
        with open(instance_file_path, 'w', encoding='utf-8') as out_file:
            json.dump(eval_data, out_file, indent=2)

        print(f"✅ Successfully created: {instance_file_path}")

        # Compare data and ground_truth and output diff if needed
        try:
            is_equal = compare_json_file(instance_file_path, output_dir=output_folder)
            if not is_equal:
                print(f"✏️ Difference written for instance_{counter}.json")
        except Exception as e:
            print(f"⚠️ Failed to compare JSONs for {instance_file_path}: {str(e)}")

        counter += 1  # Increment the global counter after each file is created
