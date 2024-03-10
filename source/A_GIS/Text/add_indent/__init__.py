def add_indent(text, spaces=4):
    """Adds indentation to each line of a given text block.

    This function takes a string of text and adds an indentation (a certain number of spaces)
    to the beginning of each line using regular expressions. The result is a modified version of
    the original text with added indentation.

    Note: This function assumes that the input text uses Unix-style newlines ('
    ') for line separation.

    Args:
        text (str): The string to which indentation should be added.
        spaces (int, optional): The number of spaces by which each line should be indented.
                                 Defaults to 4 spaces if not provided.

    Returns:
        str: A new string with the same content as the input text but with each line indented
             by the specified number of spaces.
    """

    import re

    return re.sub(r"^", " " * spaces, text, flags=re.MULTILINE)
