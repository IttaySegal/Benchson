import generate_data as g
import os


def generate_all_pairs(modifications_path, output_folder, error_folder):
    themes_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'themes.txt')
    structures_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'structures.txt')

    with open(themes_file, 'r', encoding='utf-8') as f:
        themes = [line.strip() for line in f if line.strip()]

    with open(structures_file, 'r', encoding='utf-8') as f:
        structures = [line.strip() for line in f if line.strip()]

    for theme in themes:
        for structure in structures:
            g.generate_valid_data(theme, structure, modifications_path, output_folder, error_folder)


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    modifications_path = os.path.join(base_path, '..', 'lists', 'modifications_for_strict_schema.txt')

    # Output folder for successful cases
    output_folder = os.path.join(base_path, '..', 'data')
    # Error folder for failed cases
    error_folder = os.path.join(base_path, '..', 'errors')

    # Ensure both output and error folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)

    generate_all_pairs(modifications_path, output_folder, error_folder)
