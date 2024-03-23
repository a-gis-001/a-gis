def reformat(docstring: str) -> str:
    """Reformat a docstring according to PEP 257.

    - Split out the first sentence and show as description.
    - Wrap and indent text to fill 72 chars, preserving paragraph breaks.
    """
    import re
    import textwrap
    import A_GIS.Text.split_first_sentence  
    import A_GIS.Text.replace_block

    # Split the first sentence
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(
        text=docstring
    )
    first_sentence = first_sentence.strip()
    remaining_text = textwrap.dedent(remaining_text).strip()

    # Pattern to match code blocks or preformatted text
    # This is a simple heuristic and might need adjustment for complex cases
    code_block_pattern = r'(```[\s\S]*?```)'  # Matches fenced code blocks
    code_blocks = re.findall(code_block_pattern, remaining_text)
    placeholders = [f"CODE_BLOCK_{i}" for i in range(len(code_blocks))]

    # Temporarily replace code blocks with placeholders
    for placeholder, block in zip(placeholders, code_blocks):
        remaining_text = remaining_text.replace(block, placeholder, 1)

    # Process each paragraph separately to preserve paragraph breaks
    paragraphs = remaining_text.split('\n\n')
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        wrapped_paragraph = textwrap.fill(paragraph, width=68)
        wrapped_paragraphs.append(wrapped_paragraph)
    
    # Join processed paragraphs with double newline and indent
    wrapped_and_indented_text = '\n\n'.join(['    ' + paragraph.replace('\n', '\n    ') for paragraph in wrapped_paragraphs])

    # Reinsert code blocks into their original positions
    for placeholder, block in zip(placeholders, code_blocks):
        wrapped_and_indented_text = A_GIS.Text.replace_block(
            text=wrapped_and_indented_text,find_block=placeholder,replace_with=block)

    # Construct final docstring
    if wrapped_and_indented_text.strip():
        docstring = f"{first_sentence}\n\n{wrapped_and_indented_text}\n    "
    else:
        docstring = first_sentence

    return docstring
