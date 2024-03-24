def to_string(*, docstring: type["A_GIS.Code.Docstring._Docstring"]):
    """Render docstring as a string"""
    import docstring_parser

    text = docstring_parser.compose(
        docstring,
        style=docstring_parser.DocstringStyle.GOOGLE,
        rendering_style=docstring_parser.RenderingStyle.EXPANDED,
    )
    return text
