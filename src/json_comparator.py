import json
import os
import re
from deepdiff import DeepDiff

def classify_diff(diff):
    """
    Classify the type of difference found in a JSON comparison.

    Args:
        diff (DeepDiff): The DeepDiff output.

    Returns:
        str: A string representing the classification of the difference.
    """
    if not diff:
        return "No difference"

    if 'dictionary_item_added' in diff or 'dictionary_item_removed' in diff:
        return "Structural change (keys added/removed)"
    if 'type_changes' in diff:
        return "Data type change"
    if 'values_changed' in diff:
        return "Value change"
    if 'iterable_item_added' in diff or 'iterable_item_removed' in diff:
        return "Array structure change"
    if 'set_item_added' in diff or 'set_item_removed' in diff:
        return "Set structure change"
    return "Unclassified difference"


def clean_deepdiff_paths(diff_dict):
    """
    Clean DeepDiff paths by removing 'root' and any array indices like [0], [1], etc.
    Also format changes clearly (old -> new) for value and type changes.

    Args:
        diff_dict (dict): A DeepDiff dictionary already converted from .to_json().

    Returns:
        dict: A cleaned and formatted diff dictionary.
    """
    cleaned_diff = {}

    for change_type, changes in diff_dict.items():
        cleaned_changes = []

        if change_type == "values_changed":
            for path, change in changes.items():
                # Remove root
                if path.startswith("root"):
                    path = path[len("root"):]
                # Remove array indices
                path = re.sub(r"\[\d+\]", "", path)

                old_value = change.get("old_value")
                new_value = change.get("new_value")
                cleaned_changes.append(f"{path.strip()} changed from {repr(old_value)} to {repr(new_value)}")

        elif change_type == "type_changes":
            for path, change in changes.items():
                if path.startswith("root"):
                    path = path[len("root"):]
                path = re.sub(r"\[\d+\]", "", path)

                old_type = change.get("old_type")
                new_type = change.get("new_type")
                cleaned_changes.append(f"{path.strip()} type changed from {old_type} to {new_type}")

        else:
            # For adds/removes: simple list of paths
            for path in changes:
                if path.startswith("root"):
                    path = path[len("root"):]
                path = re.sub(r"\[\d+\]", "", path)
                cleaned_changes.append(path.strip())

        cleaned_diff[change_type] = cleaned_changes

    return cleaned_diff


def compare_json_object(eval_data, diffs_folder=None, instance_id=None):
    """
    Compare 'data' and 'ground_truth' from an eval_data object.
    If differences are found, write them to a corresponding diff_output_X.txt file.

    Args:
        eval_data (dict): The JSON evaluation data containing 'data' and 'ground_truth'.
        diffs_folder (str or None): Directory to save diffs if needed.
        instance_id (str or None): Optional ID to name output files uniquely.

    Returns:
        bool: True if the data matches ground_truth, False otherwise.
    """
    data = eval_data.get("data")
    ground_truth = eval_data.get("ground_truth")

    if data is None or ground_truth is None:
        raise ValueError("Missing 'data' or 'ground_truth' in eval_data.")

    diff = DeepDiff(data, ground_truth, False)  #TODO: check if order in lists matters in this project

    if not diff:
        return True

    diff_classification = classify_diff(diff)

    output_path = os.path.join(diffs_folder, f"diff_output_{instance_id}.txt")

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"Diff classification: {diff_classification}\n\n")
        diff_dict = json.loads(diff.to_json())
        cleaned_diff = clean_deepdiff_paths(diff_dict)
        out.write(json.dumps(cleaned_diff, indent=2, ensure_ascii=False))

    return False

