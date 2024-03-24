def reformat(*, docstring: str, width: int = 72) -> str:
    """Reformat a docstring according to PEP 257.

    - Split out the first sentence and show as description.
    - Wrap and indent text to fill 72 chars, preserving paragraph breaks.
    """
    import re
    import textwrap
    import A_GIS.Text.split_first_sentence
    import A_GIS.Text.replace_block
    import A_GIS.Text.insert_block_placeholders
    import A_GIS.Text.reconstitute_blocks
    import docstring_parser

    # Parse the docstring
    parsed = docstring_parser.parse(docstring)

    # Add placeholders inside blocks inside description for wrapping.
    subs, wrapped_and_indented_text = A_GIS.Text.insert_block_placeholders(
        text=parsed.long_description, block_name=r"\S*"
    )

    # Wrap parameter descriptions.
    for i in range(len(parsed.params)):
        parsed.params[i].description = (
            textwrap.fill(parsed.params[i].description, width) + "\n"
        )

    #     # Process each paragraph separately to preserve paragraph breaks
    paragraphs = wrapped_and_indented_text.split("\n\n")
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        wrapped_paragraph = textwrap.fill(
            textwrap.dedent(paragraph), width=width - 4
        )
        wrapped_paragraphs.append(wrapped_paragraph)

    # Join processed paragraphs with double newline and indent
    wrapped_and_indented_text = "\n\n".join(wrapped_paragraphs)

    # Reinsert code blocks into their original positions
    parsed.long_description = A_GIS.Text.reconstitute_blocks(
        text=wrapped_and_indented_text, subs=subs
    )

    # Construct and return final docstring.
    docstring = docstring_parser.compose(
        parsed,
        style=docstring_parser.DocstringStyle.GOOGLE,
        rendering_style=docstring_parser.RenderingStyle.EXPANDED,
    )
    docstring = textwrap.indent(docstring, "    ")
    docstring = docstring.lstrip()
    return docstring
