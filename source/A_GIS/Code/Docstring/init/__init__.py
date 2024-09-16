def init(
    *, text: str, reference_code: str = None
) -> type["A_GIS.Code.Docstring._Docstring"]:
    """Initialize a `Docstring` object with text code reference.

    The `init` function takes a single required argument, `text`, which is a
    string containing the content of the docstring to be initialized. An
    optional argument, `reference_code`, is also accepted, which is a string
    that can be used to reference the source code associated with this
    docstring. If `reference_code` is not provided, it defaults to `None`.
    This function returns an instance of the `Docstring` class from the
    `A_GIS.Code.Docstring` module, initialized with the provided `text` and
    `reference_code`.

    Args:
        text (str):
            A string representing the docstring to be initialized. It should contain
            valid Python docstring content.
        reference_code (str, optional):
            An optional string that can be used to reference the source code
            associated with this docstring. Defaults to `None` if not provided.

    Returns:
        A_GIS.Code.Docstring._Docstring:
            An instance of the `Docstring` class containing the
            initialized docstring and its optional reference to the source code.
    """

    import A_GIS.Code.Docstring._Docstring

    return A_GIS.Code.Docstring._Docstring(
        text=text, reference_code=reference_code
    )
