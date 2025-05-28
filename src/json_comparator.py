import json
import os
import re
from deepdiff import DeepDiff

from deepdiff import DeepDiff

def classify_diff(data, ground_truth, modification_type=None):
    """
    Run DeepDiff on the input data with conditional order sensitivity based on a modification type.

    Args:
        data (dict): Original JSON data.
        ground_truth (dict): Modified JSON data.
        modification_type (str): Description of the modification applied.

    Returns:
        tuple[str, DeepDiff]: Classification label and the raw diff object.
    """
    order_sensitive = ["order","duplicate"] # currently only "order" is relevant

    ignore_order = not any(keyword.lower() in modification_type.lower() for keyword in order_sensitive)

    diff = DeepDiff(data, ground_truth, ignore_order=ignore_order)

    if not diff:
        return "No difference", diff

    if 'dictionary_item_added' in diff or 'dictionary_item_removed' in diff:
        return "Structural change (keys added/removed)", diff
    if 'type_changes' in diff:
        return "Data type change", diff
    if 'values_changed' in diff:
        return "Value change", diff
    if 'iterable_item_added' in diff or 'iterable_item_removed' in diff:
        return "Array structure change", diff
    if 'set_item_added' in diff or 'set_item_removed' in diff:
        return "Set structure change", diff

    return "Unclassified difference", diff



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
            # For adds/removes: a simple list of paths
            for path in changes:
                if path.startswith("root"):
                    path = path[len("root"):]
                path = re.sub(r"\[\d+\]", "", path)
                cleaned_changes.append(path.strip())

        cleaned_diff[change_type] = cleaned_changes

    return cleaned_diff


def compare_json_object(eval_data, diffs_folder=None, instance_id=None, modification_type=None):
    data = eval_data.get("data")
    ground_truth = eval_data.get("ground_truth")

    if data is None or ground_truth is None:
        raise ValueError("Missing 'data' or 'ground_truth' in eval_data.")

    classification, diff = classify_diff(data, ground_truth, modification_type)

    if not diff:
        return True

    output_path = os.path.join(diffs_folder, f"diff_output_{instance_id}.txt")
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"Diff classification: {classification}\n\n")
        diff_dict = json.loads(diff.to_json())
        cleaned_diff = clean_deepdiff_paths(diff_dict)
        out.write(json.dumps(cleaned_diff, indent=2, ensure_ascii=False))

    return False


