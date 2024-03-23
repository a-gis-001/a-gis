def reformat(docstring: str) -> str:
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
    
    # Split the first sentence
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(
        text=docstring
    )
    first_sentence = first_sentence.strip()
    remaining_text = textwrap.dedent(remaining_text).strip()

    # Add placeholders.
    subs,ntext = A_GIS.Text.insert_block_placeholders(text=remaining_text,block_name=r"\S*")

    # Process each paragraph separately to preserve paragraph breaks
    paragraphs = ntext.split("\n\n")
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        wrapped_paragraph = textwrap.fill(textwrap.dedent(paragraph), width=68)
        wrapped_paragraphs.append(wrapped_paragraph)

    # Join processed paragraphs with double newline and indent
    wrapped_and_indented_text = "\n\n".join(wrapped_paragraphs)
    wrapped_and_indented_text = textwrap.indent(wrapped_and_indented_text,'    ')

    # Reinsert code blocks into their original positions
    rtext = A_GIS.Text.reconstitute_blocks(text=wrapped_and_indented_text,subs=subs)

    # Construct final docstring
    if rtext.strip():
        docstring = f"{first_sentence}\n\n{rtext}\n    "
    else:
        docstring = first_sentence

    return docstring
