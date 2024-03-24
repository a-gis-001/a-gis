def to_string(
    *, docstring: type["A_GIS.Code.Docstring._Docstring"], indent="    "
):
    """Render docstring as a string"""
    import docstring_parser
    import textwrap

    text = docstring_parser.compose(
        docstring,
        style=docstring_parser.DocstringStyle.GOOGLE,
        rendering_style=docstring_parser.RenderingStyle.EXPANDED,
    )

    # Indent all but the first line.
    text = textwrap.indent(text, indent).lstrip()

    return text
