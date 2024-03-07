def highlight(*, code: str) -> str:
    """
    Highlights Python code syntax for terminal or non-terminal environments.

    This function dynamically chooses the appropriate formatter based on the execution environment
    (terminal or non-terminal) and applies syntax highlighting to the provided Python code.

    Args:
        code (str): The Python code to highlight.

    Returns:
        str: The highlighted Python code as a string.

    """
    # Dynamically import necessary modules inside the function
    import pygments
    import pygments.lexers
    import pygments.formatters
    import sys

    # Determine the appropriate formatter based on the execution environment
    if sys.stdout.isatty():
        formatter = pygments.formatters.TerminalFormatter()
    else:
        formatter = pygments.formatters.NullFormatter()

    # Apply syntax highlighting to the code using the determined formatter
    return pygments.highlight(code, pygments.lexers.PythonLexer(), formatter)
