def get_before_tag(*, text: str, tag: str):
    """Extract substring before specified tag.

    This function finds the first occurrence of a given tag within a provided text and returns
    everything before it, including the tag itself. If the tag is not found in the text,
    the original text is returned unchanged.

    Args:
        text (str): The input string to search for the tag in.
        tag (str): The specific tag to find within the text.

    Returns:
        str: The part of the original text that precedes the specified tag, or
             the original text if the tag is not found.
    """

    t = text.find(tag)
    if t >= 0:
        text = text[:t]
    return text
