def is_program(*, code: str, filename: str = ""):
    """Checks whether a piece of code is considered a program or not.

    This function takes as input a string containing the source code and an optional filename.
    It determines if the file is named "__main__.py" or contains "sys.argv", which are common indicators of a standalone script in Python.
    If either condition is met, it returns True; otherwise, it returns False.

    Args:
        code (str): The source code to be checked.
        filename (str, optional): The name of the file containing the code. Defaults to an empty string.

    Raises:
        None

    Returns:
        bool: True if the code is considered a program; False otherwise.
    """

    # Checks if file is named __main__.py or contains sys.argv
    if filename == "__main__.py":
        return True

    if "sys.argv" in code:
        return True

    return False
