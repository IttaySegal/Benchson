import json
from json import JSONDecodeError
from jsonschema import Draft7Validator, exceptions, validate


def json_schema_validator(schema: dict) -> bool:
    """
    Validates a JSON schema dict to ensure it conforms to the JSON Schema Draft 7 specification.

    Args:
        schema (dict): The JSON schema.

    Returns:
        bool: True if the schema is valid, False otherwise.
    """
    try:
        Draft7Validator.check_schema(schema)
        return True
    except exceptions.SchemaError:
        return False


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