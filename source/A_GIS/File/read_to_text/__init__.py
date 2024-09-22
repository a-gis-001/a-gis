import pathlib

def read_to_text(*, path: pathlib.Path | str, beginchar=0, endchar=-1):
    """Read text from a given path, extracts a substring if specified, and returns the content as a structured dataclass object with path details.

    A function that reads text from a given path and returns it as a
    structured dataclass object.

    This function first determines whether the `path` provided is a URL or a
    local file path using the helper function `is_url`. It then reads the
    text content from the specified path, optionally extracting a substring
    between `beginchar` and `endchar`. The extracted text, along with the
    original path and the indices specifying the substring range, are
    encapsulated in a dataclass instance.

    Args:
        - path (pathlib.Path | str):
            The file path or URL from which to read the text content. If a string,
            it can be either a path or a URL.
        - beginchar (int, optional):
            The starting index of the substring to be extracted from the text
            content. Defaults to 0.
        - endchar (int, optional):
            The ending index of the substring to be extracted from the text content.
            Defaults to -1, which means the entire text is used.

    Returns:
        dataclass:
            A 'Result' dataclass instance with the following attributes:
            - text (str): The extracted substring of the text content.
            - path (str): The resolved file path as a string.
            - beginchar (int): The starting index of the extracted substring within the text content.
            - endchar (int): The ending index of the extracted substring within the text content.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct

    # Decide whether we have a URL or a filename to call the unstructured
    # partition function with the right key.
    if isinstance(path, pathlib.Path):
        key = "filename"
    elif A_GIS.File.is_url(name=path):
        key = "url"
    else:
        key = "filename"
        path = pathlib.Path(path).resolve()

    # Get the elements from unstructured.
    elements = unstructured.partition.auto.partition(**{key: str(path)})

    # Join the elements with simple double newlines.
    text = "\n\n".join(map(str, elements))

    # Return relevant info a struct. We transform the path to a string to make sure
    # the struct can be transformed to a dict or JSON easily.
    return A_GIS.Code.make_struct(
        text=text[beginchar:endchar],
        path=str(path),
        beginchar=beginchar,
        endchar=endchar,
    )
