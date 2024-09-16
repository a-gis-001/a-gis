def add_indent(text, spaces=4):
    """Add indent to a text block.

    The `add_indent` function takes a string containing multiple lines of
    code or text and adds a specified number of spaces as indentation to the
    beginning of each line. This can be used to format unindented code
    blocks or text paragraphs.

    Args:
        text (str):
            The multiline text or code block that needs to be indented.
        spaces (int, optional):
            The number of spaces to add as indentation. Default is 4.

    Returns:
        str:
            A new string with the specified indentation added to each line of the original text.
    """

    import re

    return re.sub(r"^", " " * spaces, text, flags=re.MULTILINE)
