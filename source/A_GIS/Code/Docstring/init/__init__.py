def init(*, text: str, reference_code: str = None):
    """Initialize a docstring from text."""
    import docstring_parser
    import A_GIS.Code.Docstring._Docstring

    parent = docstring_parser.parse(
        text, style=docstring_parser.DocstringStyle.AUTO
    )
    docstring = A_GIS.Code.Docstring._Docstring(
        parent=parent, reference_code=reference_code
    )
    return docstring
