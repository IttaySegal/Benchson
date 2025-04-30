import generate_data as g
import os

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    base_folder = os.path.join(base_path, '..', 'output')
    modifications_path = os.path.join(base_path, '..', 'lists', 'modifications_for_strict_schema.txt')

    themes_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'themes.txt')
    structures_file = os.path.join(os.path.dirname(__file__), '..', 'lists', 'structures.txt')

    with open(themes_file, 'r', encoding='utf-8') as f:
        themes = [line.strip() for line in f if line.strip()]

    with open(structures_file, 'r', encoding='utf-8') as f:
        structures = [line.strip() for line in f if line.strip()]

    for theme in themes:
        for structure in structures:
            g.generate_data(theme, structure, modifications_path, base_folder)
