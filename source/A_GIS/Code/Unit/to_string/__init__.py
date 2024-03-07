def to_string(
    *,
    unit: type["A_GIS.Code.Unit._Unit"],
    start_index: int = 0,
):
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
                s += "|TYP|{}".format(A_GIS.Code.Unit.highlight(l))
            s += border

    # Emit the function signature.
    if not unit.function_definition is None:
        s += border
        for b in unit.function_definition or []:
            s += "|DEF|{}".format(A_GIS.Code.Unit.highlight(b))

    # Emit the docstring.
    if not unit.docstring is None:
        s += border
        for b in unit.docstring or []:
            s += "|DOC|{:s}\n".format(b)

    # Emit the body.
    s += border
    for b in unit.code_body:
        for l in b:
            s += "|{:03d}|{}".format(start_index, A_GIS.Code.Unit.highlight(l))
        s += border
        start_index += 1

    # Return the string.
    return s
