import docstring_parser

class _Docstring(docstring_parser.common.Docstring):
    """Subclass docstring_parser.common.Docstring for inter-operatability"""

    def __init__(self, *, text, reference_code):
        super().__init__()

        parent = docstring_parser.parse(
            text, style=docstring_parser.DocstringStyle.AUTO
        )
        self.short_description = parent.short_description
        self.long_description = parent.long_description
        self.blank_after_short_description = (
            parent.blank_after_short_description
        )
        self.blank_after_long_description = parent.blank_after_long_description
        self.meta = parent.meta
        self.style = parent.style
        self.reference_code = reference_code

    def __repr__(self):
        import A_GIS.Code.Docstring.to_string

        return A_GIS.Code.Docstring.to_string(docstring=self)
