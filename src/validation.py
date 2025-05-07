from jsonschema import Draft7Validator, exceptions, validate
from typing import Tuple, Optional


def json_schema_validator(schema: dict) -> Tuple[bool, Optional[str]]:
    """
    Validates a JSON schema dict to ensure it conforms to the JSON Schema Draft 7 specification.
    Args:
        schema (dict): The JSON schema.
    Returns:
        bool: True if the schema is valid, False otherwise.
    """
    try:
        Draft7Validator.check_schema(schema)
        return True, None
    except exceptions.SchemaError as err:
        return False, f"SchemaError: {err.message}"

def json_validator(json_instance: dict, json_schema: dict) -> bool:
    """
    Validates a JSON instance against a given JSON schema.

    Args:
        json_instance (dict): The JSON instance.
        json_schema (dict): The JSON schema.

    Returns:
        bool: True if the JSON instance conforms to the schema, False otherwise.
    """
    try:
        validate(json_instance, json_schema)
        return True
    except exceptions.ValidationError:
        return False