def reformat(*, text: str, width: int = 72) -> str:
    """Reformat text to wrap and indent to fill specified width

    Preserves paragraph breaks and current indentation.

    Args:
        text (str): The text to reformat.
        width (int): The maximum width of each line.

    Returns:
        str: The reformatted text.
    """
    import re
    import textwrap
    import A_GIS.Text.insert_block_placeholders
    import A_GIS.Text.reconstitute_blocks

    # Remove extra newlines.
    text, _ = re.subn(r"\n\n+", r"\n\n", text)
    text = text.rstrip()

    # Add placeholders inside blocks inside description for wrapping.
    subs, wrapped_and_indented_text = A_GIS.Text.insert_block_placeholders(
        text=text, block_name=r"\S*"
    )

    # Process each paragraph separately to preserve paragraph breaks.
    paragraphs = wrapped_and_indented_text.split("\n\n")
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        # Check if any line in the paragraph exceeds the max line limit
        if any(len(line) > (width - 4) for line in paragraph.splitlines()):
            # If so, wrap the entire paragraph
            wrapped_paragraph = textwrap.fill(
                textwrap.dedent(paragraph), width=width - 4
            )
        else:
            # Otherwise, just dedent without wrapping
            wrapped_paragraph = textwrap.dedent(paragraph)
        wrapped_paragraphs.append(wrapped_paragraph)

    # Join processed paragraphs with double newline and indent
    wrapped_and_indented_text = "\n\n".join(wrapped_paragraphs)

    # Reinsert code blocks into their original positions
    reformatted_text = A_GIS.Text.reconstitute_blocks(
        text=wrapped_and_indented_text, subs=subs
    )

    return reformatted_text
