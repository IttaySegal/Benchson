from generate_data import generate_data
import os

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    base_folder = os.path.join(base_path, '..', 'data')
    os.makedirs(base_folder, exist_ok=True)

    themes_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'themes.txt')
    structures_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'structures.txt')

    with open(themes_file, 'r', encoding='utf-8') as f:
        themes = [line.strip() for line in f if line.strip()]

    with open(structures_file, 'r', encoding='utf-8') as f:
        structures = [line.strip() for line in f if line.strip()]

    schema_types = ["strict", "dynamic", "strict"]

    for  schema_type in schema_types:
        folder = os.path.join(base_folder, f'data_{schema_type}_schema')
        os.makedirs(folder, exist_ok=True)
        modifications_dynamic_schema_path = os.path.join(base_path, '..', 'lists', f'modifications_for_{schema_type}_schema.txt')

        counter = 0
        for theme in themes:
            for structure in structures:
                c = generate_data(counter, theme, structure, modifications_dynamic_schema_path, folder, schema_type)
                counter += c
