def is_class(*, code: str):
    """Checks if a given Python code string contains a class definition but not a function definition.

    The function uses regular expressions to search for the presence of 'class' at the start of a line (not preceded by any whitespace),
    indicating that it is likely a class definition, and no instances of 'def', which would indicate a function definition.

    Args:
        code (str): A string containing Python code to be checked.

    Raises:
        None

    Returns:
        bool: True if the provided code contains a class definition but not a function definition, otherwise False.
    """

    # Matches `class` at the start of a line, with no leading whitespace
    import re

    result = bool(
        re.search(r"^class ", code, flags=re.MULTILINE)
    ) and not bool(re.search(r"^def ", code, flags=re.MULTILINE))

    return result
