import json
from validation import json_schema_validator, json_validator
from LLMJsonGenerator import LLMJsonGenerator
import os

if __name__ == "__main__":
    generator = LLMJsonGenerator()

    structure = "Basic Item List: A straightforward, one-level list where each entry includes properties like ID, name, and description."
    theme = "Learning Algorithms"
    modifications_path = os.path.join(os.path.dirname(__file__), '..', 'lists', 'specific_modifications.txt')
    output_path = os.path.join(os.path.dirname(__file__), '..', 'lists', 'modification_outputs.txt')

    # Read modification types from file
    with open(modifications_path, 'r', encoding='utf-8') as f:
        modifications = [line.strip() for line in f if line.strip()]

    # Start new output file
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write("=== Modification Results ===\n\n")
        out_file.write(f"Theme: {theme}\n")
        out_file.write(f"Structure: {structure}\n\n")

        out_file.write("Generating JSON schema...\n")
        json_schema = generator.json_schema_generator(theme, structure)
        if not json_schema_validator(json_schema):
            out_file.write("❌ JSON schema not valid.\n")
            exit()
        out_file.write("✅ JSON Schema generated:\n")
        out_file.write(json.dumps(json_schema, indent=2) + "\n\n")

        # Loop over modifications
        for modification_type in modifications:
            out_file.write(f"--- Modification: {modification_type} ---\n\n")

            # Generate original JSON
            origin_json = generator.json_generator(json_schema, 1)
            if not json_validator(origin_json, json_schema):
                out_file.write("❌ Original JSON not valid against schema.\n\n")
                continue
            out_file.write("Original JSON:\n")
            out_file.write(json.dumps(origin_json, indent=2) + "\n\n")

            # Modify JSON
            modified_json = generator.modified_json_generator(origin_json, modification_type)
            out_file.write("Modified JSON:\n")
            out_file.write(json.dumps(modified_json, indent=2) + "\n\n")

            # Generate description
            description = generator.description_output_generator(origin_json, modified_json)
            out_file.write("Description of Modification:\n")
            out_file.write(description + "\n")

            # Validate modified JSON
            if not json_validator(modified_json, json_schema):
                out_file.write("❌ Modified JSON is INVALID against schema.\n")
            else:
                out_file.write("✅ Modified JSON is VALID.\n")

            out_file.write("\n" + "-" * 80 + "\n\n")
