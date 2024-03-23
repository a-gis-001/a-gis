def split_first_sentence(*, text: str):
    """Split the first sentence from the text.

    The result of this function is guaranteed that first_sentence +
    remaining_text == text.

    Returns:
        first_sentence, remaining_text
    """
    import spacy
    import A_GIS.Text.get_indent  # Adjust this import as necessary.

    nlp = spacy.load("en_core_web_sm")

    indent = A_GIS.Text.get_indent(line=text)
    stripped_text = text.lstrip()
    doc = nlp(stripped_text)
    sentences = list(doc.sents)

    # Remove trailing whitespace from the first sentence
    # Get the removed trailing whitespace
    # Prepend removed whitespace to remaining text
    if sentences:
        end_pos = sentences[0].end_char
        first_sentence = stripped_text[:end_pos].rstrip()
        remaining_whitespace = stripped_text[:end_pos][len(first_sentence) :]
        remaining_text = remaining_whitespace + stripped_text[end_pos:]

    # Just assume the first sentence is nothing.
    else:
        first_sentence = ""
        remaining_text = stripped_text

    # Add back the indent.
    first_sentence = (" " * indent) + first_sentence

    # Return the first and remaining text.
    return first_sentence, remaining_text
