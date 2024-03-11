def is_function(*, code: str):
    """Checks if a given piece of Python code is a function or not.

    This function checks whether the provided Python code represents a function
    by searching for the 'def' keyword at the start of a line, indicating the
    beginning of a function definition. It also ensures that this code does not
    represent a class definition by checking for the 'class' keyword.

    Args:
        code (str): The Python code to be checked.

    Raises:
        None

    Returns:
        bool: True if the provided code is a function, False otherwise.
    """

    import re

    # Matches `def` at the start of a line, with no leading whitespace
    return bool(re.search(r"^def ", code, flags=re.MULTILINE)) and not bool(
        re.search(r"^class ", code, flags=re.MULTILINE)
    )
