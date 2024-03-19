def find_and_replace(*, text: str, old: str, new: str, is_regex: bool = False):
    """
    Find and replace in file. Can use plain strings or regular expressions.
    Returns the total number of replacements made across all files.

    Parameters:
    - files: List of Path objects pointing to files where replacements should be made.
    - old: The string or regular expression to find.
    - new: The string to replace with.
    - is_regex: If True, treat `old` as a regular expression. Otherwise, treat as plain string.
    """
    import re

    # Perform replacement and count occurrences
    if is_regex:
        text, replacements = re.subn(old, new, text)
    else:
        replacements = text.count(old)
        text = text.replace(old, new)

    return text, replacements
