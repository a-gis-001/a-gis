def check_short_description(*, short_description: str):
    """Check that the short description meets standards

    The standards are as follows.

    - Is a string.
    - No more than 64 characters.
    - Starts with a verb.
    - Starts with the simplest stem of that verb.
    - Starts with capitalization.
    - Ends with a period.
    - No whitespace at the end.

    """
    import A_GIS.Text.get_root_word
    import A_GIS.Text.starts_with_verb

    # Check and abort if not a string.
    errors = []
    if not isinstance(short_description, str):
        errors.append("Not a string")
        return errors

    # Check length.
    length = len(short_description)
    if length > 64:
        errors.append(f"Length ({length}) must be 64 characters or less.")

    # Add check for ends with a period.
    if not short_description.endswith("."):
        errors.append("Does not end with a period.")

    # Add check for no whitespace at end.
    if short_description != short_description.rstrip():
        errors.append("Ends with whitespace.")

    # Check capitalization.
    if short_description[0] != short_description[0].upper():
        errors.append("Not capitalized.")

    # Check starts with verb.
    if not A_GIS.Text.starts_with_verb(sentence=short_description).result:
        errors.append(f"Does not start with a verb.")

    # Check simplest form of verb.
    first = short_description.split(" ")[0].lower()
    stem = A_GIS.Text.get_root_word(word=first).lower()
    if stem != first:
        errors.append(
            f"Verb is not a simple stem (found '{first}', should be '{stem}')."
        )

    return errors
