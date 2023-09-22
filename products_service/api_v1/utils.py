import ulid


def is_valid_ulid(ulid_string):
    """Validates a string is of type ULID"""
    try:
        ulid.from_str(ulid_string)
        return True
    except ValueError:
        return False


def serialize_ULID(representation):
    """
    Converts ULID fields to their string representations in the response payload.

    This function traverses the response payload and converts any ULID fields to
    their string representations.

    Parameters:
        representation (dict): The response payload represented as a dictionary.

    Returns:
        dict: The updated response payload with ULID fields converted to strings.
    """
    for field, value in representation.items():
        if isinstance(value, ulid.ULID):
            representation[field] = str(value)
        if isinstance(value, list):
            new_list = [str(i) for i in value if isinstance(i, ulid.ULID)]
            representation[field] = new_list
    return representation
