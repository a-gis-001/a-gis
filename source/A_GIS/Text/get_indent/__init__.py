def get_indent(*, line: str) -> int:
    """Gets the indentation of a line in a string.

    This function takes a single argument, `line`, which is expected to be a string. It returns
    the number of leading spaces or tabs at the beginning of the string. This can be used to
    determine the level of indentation for a given line of text.

    Args:
        line (str): The input string from which to determine indentation.

    Raises:
        None

    Returns:
        int: The number of leading spaces or tabs in `line`.
    """

    return len(line) - len(line.lstrip())
