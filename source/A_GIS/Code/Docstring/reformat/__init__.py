def reformat(
    *, docstring: type["A_GIS.Code.Docstring._Docstring"], width: int = 72
) -> str:
    """Reformat a docstring according to PEP 257.

    - Split out the first sentence and show as description.
    - Wrap and indent text to fill 72 chars, preserving paragraph breaks.

    Args:
        docstring (Docstring):
            The docstring object to reformat.
        width (int):
            The maximum line width for formatting.

    Returns:
        Docstring:
            The reformatted docstring object.
    """

    import A_GIS.Text.split_first_sentence
    import A_GIS.Text.reformat
    import A_GIS.Text.get_indent
    import textwrap

    # Initialize empty descriptions if none exist.
    if docstring.short_description is None:
        docstring.short_description = ""
    if docstring.long_description is None:
        docstring.long_description = ""

    # Extract the first sentence for the short description.
    first, other = A_GIS.Text.split_first_sentence(
        text=docstring.short_description
    )
    docstring.short_description = first

    # Append remaining content to the long description if there is more.
    if other.strip() != "":
        other = other + "\n\n"
    docstring.long_description = other + docstring.long_description

    # Ensure proper formatting flags.
    docstring.blank_after_short_description = True
    docstring.blank_after_long_description = True

    # Reformat the long description text using Text.reformat
    docstring.long_description = A_GIS.Text.reformat(
        text=docstring.long_description, width=width - 4
    )

    def rewrap_description(d):
        return A_GIS.Text.reformat(text=d, width=width - 12)

    # Wrap and indent parameter descriptions.
    for i in range(len(docstring.params)):
        docstring.params[i].description = rewrap_description(
            docstring.params[i].description
        )

    # Wrap and indent return description.
    docstring.returns.description = rewrap_description(
        docstring.returns.description
    )

    return docstring
