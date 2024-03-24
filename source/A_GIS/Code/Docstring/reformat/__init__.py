def reformat(
    *, docstring: type["A_GIS.Code.Docstring._Docstring"], width: int = 72
) -> str:
    """Reformat a docstring according to PEP 257.

    - Split out the first sentence and show as description.
    - Wrap and indent text to fill 72 chars, preserving paragraph breaks.
    """
    import re
    import textwrap
    import A_GIS.Text.insert_block_placeholders
    import A_GIS.Text.reconstitute_blocks
    import A_GIS.Text.split_first_sentence

    # Set as empty.
    if docstring.short_description is None:
        docstring.short_description = ""
    if docstring.long_description is None:
        docstring.long_description = ""

    # Only keep the first sentence in short.
    first, other = A_GIS.Text.split_first_sentence(
        text=docstring.short_description
    )
    docstring.short_description = first
    other = other.strip()
    if other != "":
        other = other + "\n\n"
    docstring.long_description = other + docstring.long_description

    # Remove extra newlines.
    docstring.long_description, _ = re.subn(
        r"\n\n+", r"\n\n", docstring.long_description
    )
    docstring.long_description = docstring.long_description.rstrip()

    # Add formatting options.
    docstring.blank_after_short_description = True
    docstring.blank_after_long_description = True

    # Add placeholders inside blocks inside description for wrapping.
    subs, wrapped_and_indented_text = A_GIS.Text.insert_block_placeholders(
        text=docstring.long_description, block_name=r"\S*"
    )

    # Wrap parameter descriptions.
    for i in range(len(docstring.params)):
        docstring.params[i].description = (
            textwrap.fill(docstring.params[i].description, width) + "\n"
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
    docstring.long_description = A_GIS.Text.reconstitute_blocks(
        text=wrapped_and_indented_text, subs=subs
    )

    return docstring
