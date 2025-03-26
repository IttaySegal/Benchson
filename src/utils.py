import random

def get_random_structure(file_path="../lists/structures.txt"):
    with open(file_path, "r") as f:
        structures = [line.strip() for line in f if line.strip()]
    return random.choice(structures)

def get_random_theme(file_path="../lists/themes.txt"):
    with open(file_path, "r") as f:
        themes = [line.strip() for line in f if line.strip()]
    return random.choice(themes)

def get_random_modification(file_path="../lists/modifications.txt"):
    with open(file_path, "r") as f:
        modifications = [line.strip() for line in f if line.strip()]
    return random.choice(modifications)