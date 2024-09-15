def reformat(
    *, docstring: type["A_GIS.Code.Docstring._Docstring"], width: int = 72
) -> str:
    """Reformat a docstring according to PEP 257.

    - Split out the first sentence and show as description.
    - Wrap and indent text to fill 72 chars, preserving paragraph breaks.
    """
    import A_GIS.Text.split_first_sentence
    import A_GIS.Text.reformat
    import textwrap

    # Set as empty.
    if docstring.short_description is None:
        docstring.short_description = ""
    if docstring.long_description is None:
        docstring.long_description = ""

    # Only keep the first sentence in short.
    first, other = A_GIS.Text.split_first_sentence(
        text=docstring.short_description
    )
    docstring.short_description = first
    other = other.strip()
    if other != "":
        other = other + "\n\n"
    docstring.long_description = other + docstring.long_description

    # Add formatting options.
    docstring.blank_after_short_description = True
    docstring.blank_after_long_description = True

    # Reformat the long description text
    docstring.long_description = A_GIS.Text.reformat(
        text=docstring.long_description, width=width
    )

    # Wrap parameter descriptions.
    for i in range(len(docstring.params)):
        docstring.params[i].description = (
            textwrap.fill(docstring.params[i].description, width) + "\n"
        )

    return docstring
