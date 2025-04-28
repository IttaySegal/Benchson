import json
import os
import re
from deepdiff import DeepDiff


def compare_json_data(data, ground_truth, ignore_order=False):
    """
    Compare two JSON-compatible Python objects using DeepDiff.

    Args:
        data (dict or list): Original JSON data.
        ground_truth (dict or list): Expected JSON after modification.
        ignore_order (bool): Whether to ignore array ordering.

    Returns:
        DeepDiff: Differences found by DeepDiff (empty if equal).
    """
    return DeepDiff(data, ground_truth, ignore_order=ignore_order)


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


def compare_json_file(file_path, output_dir=None):
    """
    Compare 'data' and 'ground_truth' from a JSON file.
    If differences are found, write them to a corresponding diff_output_X.txt file.

    Args:
        file_path (str): Path to the JSON file to compare.
        output_dir (str or None): Optional root directory to save output folders.
                                  If None, uses the same directory as file_path.

    Returns:
        bool: True if the data matches ground_truth, False otherwise.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)

    data = full_data.get("data")
    ground_truth = full_data.get("ground_truth")

    if data is None or ground_truth is None:
        raise ValueError("Missing 'data' or 'ground_truth' in the file.")

    diff = compare_json_data(data, ground_truth)

    if not diff:
        return True

    diff_classification = classify_diff(diff)

    # Parse instance ID
    base_name = os.path.basename(file_path)  # e.g., instance_1.json
    instance_id = os.path.splitext(base_name)[0].split("_")[-1]  # extract "1"

    # Create diffs folder
    if output_dir is None:
        output_dir = os.path.dirname(file_path)
    diffs_folder = os.path.join(output_dir, "diffs")
    os.makedirs(diffs_folder, exist_ok=True)

    # Full diff output path
    output_path = os.path.join(diffs_folder, f"diff_output_{instance_id}.txt")

    # Write diff and classification to file
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"Diff classification: {diff_classification}\n\n")

        diff_dict = json.loads(diff.to_json())
        cleaned_diff = clean_deepdiff_paths(diff_dict)

        out.write(json.dumps(cleaned_diff, indent=2, ensure_ascii=False))

    return False

