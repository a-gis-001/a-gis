def fix(*, name: str):
    """Fix an A_GIS code unit name to satisfy requirements

    Requirements:
            1. Parts separated with '.' as in Python.
            2. First part is 'A_GIS', always.
            3. Last part is a function name and is lower case with underscores '_' allowed.
            4. Other parts are package names and are capitalized, first letter only.
            5. There are no underscores '_' in a package name.
            6. Package names are simple, generic nouns.
            7. The first word in a function name is a verb.
    """

    parts = name.split(".")

    # Ensure the first part is 'A_GIS'
    if parts[0].upper() != "A_GIS":
        parts.insert(0, "A_GIS")
    else:
        parts[0] = "A_GIS"

    # Process package names (capitalized, first letter only, no underscores)
    for i in range(1, len(parts) - 1):  # Exclude the first and last parts
        part = parts[i]
        part = part.replace("_", "")  # Remove underscores
        part = part.capitalize()  # Capitalize first letter only
        parts[i] = part

    # Ensure the last part (function name) is in lower case
    parts[-1] = parts[-1].lower()

    # Re-join and return the fixed name
    fixed_name = ".".join(parts)
    return fixed_name
