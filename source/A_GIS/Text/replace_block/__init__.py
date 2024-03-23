def replace_block(
    *, text: str, find_block: str, replace_with: str, count: int = 1
) -> str:
    """
    Replace the first occurrence of a specified block of text with a new block of text within the given string.

    Args:
        text (str): The original text in which to search and replace the block.
        find_block (str): The block of text to be replaced. This block is treated as a raw string, so regular expression
                          special characters are not considered.
        replace_with (str): The block of text to insert in place of the find_block.

    Returns:
        str: The text with the first occurrence of the find_block replaced with replace_with.

    Example:
        >>> original_text = "Here is a block of text.\\nAnd here is another block."
        >>> find_block = "a block of text."
        >>> replace_with = "the replaced block."
        >>> replace_block(text=original_text, find_block=find_block, replace_with=replace_with)
        'Here is the replaced block.\\nAnd here is another block.'
    """
    # Encapsulating the import within the function
    import re

    # If a simple replacement works, do it.
    if (not "\n" in find_block) and (not "\n" in replace_with):
        return text.replace(find_block,replace_with,count)
    
    # Splitting the input text and find_block into lines for line-by-line
    # handling
    original_lines = text.splitlines()
    block_lines = find_block.strip().splitlines()

    # Escaping regex special characters in the find_block to avoid regex issues
    escaped_block_lines = [re.escape(line) for line in block_lines]

    # Building a regex pattern to match the find_block with any leading
    # whitespace and capture the indentation
    block_pattern = r"^(\s*)" + r"\n\s*".join(escaped_block_lines)

    # Preparing the replacement text with indentation preserved from the
    # find_block
    indented_replacement = "".join(
        [rf"\1{x}" for x in replace_with.splitlines()]
    )

    # Performing the replacement operation with consideration for multiline
    # and dotall modes
    new_text, num_replacements = re.subn(
        block_pattern,
        indented_replacement,
        text,
        flags=re.MULTILINE | re.DOTALL,
        count=count,
    )

    # Returning the text after the replacement
    return new_text
