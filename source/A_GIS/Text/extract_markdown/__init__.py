def extract_markdown(*, text: str, block_name: str = "python") -> str:
    """
    Extracts the content between specified Markdown code block markers.

    Args:
        text (str): The input Markdown text from which to extract the content.
        block_name (str): The language specifier for the code block. Defaults to 'python'.

    Returns:
        str: The extracted content from the specified Markdown code block. Returns an empty string if no matching block is found.
    """
    import re

    # Clean preceding blank whitespace from the text
    text = re.sub(r"^\s*$", "", text, flags=re.M)

    # Pattern to match the opening and closing ``` with the optional block_name
    # and capture the content in between. It supports optional spaces after
    # ``` for the opening marker.
    pattern = rf"```{block_name}\s*\n?([\s\S]*?)\n?```"
    match = re.search(pattern, text, flags=re.MULTILINE)

    if match:
        text = match.group(1).strip()

    return text
