def extract_markdown(
    *,
    text: str,
    block_name: str = "python",
    content_only: bool = True,
    opening: str = "```",
    closing: str = "```",
    dedent_result: bool = False,
) -> str:
    """
    Extracts the content between specified Markdown code block markers, preserving
    the relative indentation of the content.

    Args:
        text (str): The input Markdown text from which to extract the content.
        block_name (str): The language specifier for the code block. Defaults to 'python'.
        opening (str): The opening marker for the code block.
        closing (str): The closing marker for the code block.

    Returns:
        str: The extracted content from the specified Markdown code block, preserving relative indentation.
        str: The block name extracted, if any; otherwise, returns an empty string.
    """
    import re
    import textwrap

    # Pattern to match the code blocks, capturing the optional language specifier and the content
    # It accounts for optional leading whitespace (indentation) before the
    # opening marker
    pattern = rf"^([ \t]*){opening}[ \t]*({block_name})[ \t]*\n([\s\S]*?)\n\1{closing}"

    match = re.search(pattern, text, flags=re.MULTILINE)

    if match:
        # Extract the content with preserved relative indentation
        indentation, extracted_block_name, block_content = match.groups()
        if dedent_result:
            indentation = ""
            block_content = textwrap.dedent(block_content)
        if content_only:
            return block_content
        else:
            return f"{indentation}{opening}{extracted_block_name}\n{block_content}\n{indentation}{closing}"
    else:
        return ""
