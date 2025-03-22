def to_string(
    *,
    unit: type["A_GIS.Code.Unit._Unit"],
    start_index: int = 0,
):
    """Converts a code unit into a string representation with line numbers and special markers.

    Args:
        unit: An instance of A_GIS.Code.Unit._Unit to convert
        start_index: Starting line number (default: 0)

    Returns:
        str: A string representation of the code unit with line numbers and markers
    """

    import A_GIS.Code.highlight

    # Create a border.
    border = "+---+" + "-" * 80 + "+\n"

    # Initialize.
    s = ""

    # Emit the prefix.
    if not unit.type_imports is None:
        s += border
        for b in unit.type_imports or []:
            for l in b:
                s += "|TYP|{}".format(A_GIS.Code.highlight(code=l))
            s += border

    # Emit the function signature.
    if not unit.function_definition is None:
        s += border
        for b in unit.function_definition or []:
            s += "|DEF|{}".format(A_GIS.Code.highlight(code=b))

    # Emit the docstring.
    if not unit.docstring is None:
        s += border
        for b in unit.docstring or []:
            s += "|DOC|{:s}\n".format(b)

    # Emit the body.
    s += border
    for b in unit.code_body:
        for l in b:
            s += "|{:03d}|{}".format(start_index, A_GIS.Code.highlight(code=l))
        s += border
        start_index += 1

    # Return the string.
    return s
