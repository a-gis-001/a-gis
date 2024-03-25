def find_and_replace(*, text: str, old: str, new: str, is_regex: bool = False):
    """Perform find-replace in text using flag for regex.

        This function searches for a specified string or regular
        expression in the provided text and replaces it with
        another string. The search can be performed as a plain
        string match or using regular expressions, based on the
        `is_regex` flag. It also counts the number of replacements
        made.

    Args:
        - text (str): The input text where replacements should
            be made.
        - old (str): The string or regular expression to find
            and replace.
        - new (str): The string to replace `old` with.
        - is_regex (bool, optional): If True, treat `old` as a
            regular expression. Otherwise, treat it as plain
            string. Defaults to False.

    Raises:
        None

    Returns:
        Tuple[str, int]: A tuple containing the modified text and
            the number of replacements made.
    """

    import re

    # Perform replacement and count occurrences
    if is_regex:
        text, replacements = re.subn(old, new, text)
    else:
        replacements = text.count(old)
        text = text.replace(old, new)

    return text, replacements
