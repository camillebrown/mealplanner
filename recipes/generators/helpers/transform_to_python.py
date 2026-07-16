import json
import re

def title_to_python_constant(title):
    """
    Converts a recipe title into a Python constant name.

    Args:
        title: Recipe title.

    Returns:
        str: Uppercase underscore-separated constant name.
    """
    value = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        title.upper(),
    )

    return value.strip("_") or "UNTITLED_RECIPE"

def python_string(value):
    """
    Formats a value as a valid Python string literal.

    Args:
        value: Value to format.

    Returns:
        str: JSON-compatible Python string literal.
    """
    return json.dumps(
        str(value),
        ensure_ascii=False,
    )
    
def format_serving(value):
    """
    Formats a serving multiplier without unnecessary decimal zeros.

    Args:
        value: Serving multiplier.

    Returns:
        str: Formatted serving value.
    """
    if (
        isinstance(value, float)
        and value.is_integer()
    ):
        return str(int(value))

    return str(value)