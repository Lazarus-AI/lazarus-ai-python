"""Helper function to validate user-provided args."""
import stringcase

from errors import ValidationError


def _validate_args(args: dict, valid_keys: list, ignore_keys: list = [], change_case: bool = True) -> dict:
    """Validates arguments passed by the user.

    Checks that args includes only valid or optional keys. Expecting keys in
    snake_case. Converts arguments to camelCase by default as the API expects
    keys in camelCase. Raises an error if args has undefined keys or keys not
    in snake_case.

    Args:
        args (dict): Arguments passed to library functions
        valid_keys (list): List of valid optional arguments
        ignore_keys (list, optional): List of arguments in args that don't
            need to be validated, defaults to []
        change_case (bool, optional): Boolean which is true if want to make
            the args in dictionary camel case, defaults to True
    """
    invalid_keys = []
    for key in args:
        if key not in valid_keys and key not in ignore_keys:
            invalid_keys.append(key)

    if invalid_keys:
        m = f"These fields are not valid arguments: {', '.join(invalid_keys)}"
        raise ValidationError(m)

    if change_case:
        args = _make_camel_case(args)
    return args


def _make_camel_case(args: dict) -> dict:
    """ Make args camel case for API request body

    Args:
        args (dict): Dictionary with keys that are mix of snake case and
            already camel case

    Returns:
        dict: Dictionary with only camel case keys and the same corresponding
            values as passed in
    """
    d = {}
    for key in args:
        if key == "return_ocr":
            d["returnOCR"] = args[key]
            continue
        new_key = stringcase.camelcase(key)
        d[new_key] = args[key]
    return d
