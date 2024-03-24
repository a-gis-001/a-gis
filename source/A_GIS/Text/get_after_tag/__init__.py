def get_after_tag(*, text: str, tag: str):
    """Extract string after specified tag.

    This function finds the first occurrence of the given `tag` in the input `text` and returns
    everything following it, including the tag itself. If the tag is not found in the text,
    then the original text is returned.

    Args:
        text (str): The string to search within.
        tag (str): The substring to search for in `text`.

    Raises:
        None

    Returns:
        str: A new string that includes all characters from the input string after
             the first occurrence of the specified tag. If the tag is not found,
             the original text is returned.
    """

    t = text.find(tag)
    if t >= 0:
        text = text[t + len(tag) :]
    return text
