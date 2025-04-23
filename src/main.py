import generate_data as g
import os


def generate_all_pairs(modifications_path, output_folder):
    themes_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'themes.txt')
    structures_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'structures.txt')

    with open(themes_file, 'r', encoding='utf-8') as f:
        themes = [line.strip() for line in f if line.strip()]

    with open(structures_file, 'r', encoding='utf-8') as f:
        structures = [line.strip() for line in f if line.strip()]

    for theme in themes:
        for structure in structures:
            g.generate_valid_data(theme, structure, modifications_path, output_folder)


if __name__ == "__main__":
    modifications_path = os.path.join(os.path.dirname(__file__), '..', 'lists', 'modifications_for_strict_schema.txt')
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

    generate_all_pairs(modifications_path, output_folder)
