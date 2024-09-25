def fix(*, name: str, unit_type: str = "function"):
    """Standardize A_GIS unit names.

    This function takes two parameters: `name` (a string representing
    the name to be fixed) and an optional `unit_type` (a string
    indicating the type of the unit, which can be "function", "class" or
    "package"). The function ensures that the naming conventions for
    A_GIS modules, packages, classes, and functions are adhered to.

    Args:
        name (str):
            The name of the unit to be fixed. This is expected to be in
            a dot-separated format representing different levels of a
            package or class hierarchy.
        unit_type (str, optional):
            The type of the unit being fixed. It can be one of
            "function", "class", or "package". If not provided, it
            defaults to "function".

    Returns:
        str:
            A string representing the fixed name that adheres to the
            required naming conventions. The returned value will have a
            consistent format for modules, packages, classes, and
            functions as follows:

            - For unit_type="function": All lower case, starts with
              verb, snake case (e.g., "Go_Down" -> "go_down").
            - For unit_type="class": First character underscore, then
              capitalized snake case (e.g., "_Go_Down" ->
              "_get_go_down").
            - For unit_type="package": First character upper case, no
              underscores (e.g., "a_gis.sub_package" ->
              "A_GIS.SubPackage").

    """

    def fix_package_name(part):
        """First character upper case, no underscores.
        Examples:
            - go_down --> Godown
        """
        part = part.replace("_", "")
        part = part[0].upper() + part[1:]
        return part

    def fix_class_name(part):
        """First character underscore, then capitalized snake case.
        Examples:
            - go_down --> _Go_Down
        """
        import re

        if part[0] != "_":
            part = "_" + part
        part = part.lower()
        part = re.sub(r"(_\w)", lambda match: match.group(1).upper(), part)
        return part

    def fix_function_name(part):
        """All lower case, starts with verb, snake case.
        Examples:
            - Go_Down --> go_down
            - finder -> get_finder
        """
        import A_GIS.Text.starts_with_verb

        part = part.lower()
        if not A_GIS.Text.starts_with_verb(
            sentence=part.replace("_", " ")
        ).result:
            if part.startswith("_"):
                part = "_get" + part
            else:
                part = "get_" + part

        return part

    # Get parts of the name.
    parts = name.split(".")

    # Requirement 1 (root package).
    if parts[0].upper() != "A_GIS":
        parts.insert(0, "A_GIS")
    else:
        parts[0] = "A_GIS"

    # Requirement 2 (sub packages).
    for i in range(1, len(parts) - 1):
        parts[i] = fix_package_name(parts[i])
    # Requirement 3 (dependent on unit type).
    if unit_type == "class":
        parts[-1] = fix_class_name(parts[-1])
    elif unit_type == "package":
        parts[-1] = fix_package_name(parts[-1])
    else:
        parts[-1] = fix_function_name(parts[-1])

    # Re-join and return the fixed name
    fixed_name = ".".join(parts)
    return fixed_name
