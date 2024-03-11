def clean(*, docstring: str):
    """This function cleans a given docstring by removing leading and trailing blank whitespace, outer triple quotes, optional ```python``` markers, and more complex nested code blocks. It uses regular expressions to match patterns in the input string and manipulate them accordingly. The cleaned version of the input docstring is then returned as output.

    Args:
        docstring (str): The input docstring to be cleaned.

    Returns:
        str: The cleaned version of the input docstring.

    Raises:
        None

    Notes:
        This function assumes that complex nested code blocks are represented by triple quotes or ```python``` markers, and that these blocks do not appear within the first few lines or last few lines of the docstring. If this assumption is incorrect, the cleaning process might not work as expected.
    """

    import re

    # Clean preceding blank whitespace.
    docstring = re.sub(r"^\s*$", "", docstring, flags=re.M)

    # Pattern to match outer triple quotes and optional ```python``` markers
    pattern = r'^\s*("""|```python\n?)([\s\S]*?)(\1|```)\s*$'
    match = re.match(pattern, docstring)
    if match:
        docstring = match.group(2)

    # Remove more complex nested stuff.
    def __maybe_block(line):
        return (
            line.lstrip().startswith("```")
            or line.lstrip().startswith('"""')
            or line.lstrip().startswith("'''")
        )

    lines = docstring.splitlines()
    strip_begin = 0
    strip_end = len(lines)
    for i, line in enumerate(lines):
        if strip_begin == 0 and i < 3 and __maybe_block(line):
            strip_begin = i + 1
        elif i > strip_begin and i > len(lines) - 3 and __maybe_block(line):
            strip_end = i
    lines = lines[strip_begin:strip_end]
    docstring = "\n".join(lines)

    return docstring
