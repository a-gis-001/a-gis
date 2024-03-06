def to_string(
    *,
    unit: type["A_GIS.Code.Unit._Unit"],
    start_index: int = 0,
    formatter=None,
):
    def highlight(code):
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import TerminalFormatter, NullFormatter
        import sys

        nonlocal formatter
        if formatter is None:
            if sys.stdout.isatty():
                formatter = TerminalFormatter()
            else:
                formatter = NullFormatter()
        return highlight(code, PythonLexer(), formatter)

    # Create a border.
    def border():
        return "+---+" + "-" * 80 + "+\n"

    # Initialize.
    s = ""

    # Emit the prefix.
    if not unit.type_imports is None:
        s += border()
        for b in unit.type_imports or []:
            for l in b:
                s += "|TYP|{}".format(highlight(l))
            s += border()

    # Emit the function signature.
    if not unit.function_definition is None:
        s += border()
        for b in unit.function_definition or []:
            s += "|DEF|{}".format(highlight(b))

    # Emit the docstring.
    if not unit.docstring is None:
        s += border()
        for b in unit.docstring or []:
            s += "|DOC|{:s}\n".format(b)

    # Emit the body.
    s += border()
    for b in unit.code_body:
        for l in b:
            s += "|{:03d}|{}".format(start_index, highlight(l))
        s += border()
        start_index += 1

    # Return the string.
    return s
