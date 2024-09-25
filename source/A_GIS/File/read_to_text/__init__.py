import pathlib

def read_to_text(*, path: pathlib.Path | str, beginchar=None, endchar=None):
    """Read text content from a file or URL, optionally extracting a specified character range, and returns as a dataclass instance with text,.

    A function that reads text content from a given file or URL and returns
    it as a string with optional character range extraction. It also
    determines whether the input is a file path or a URL and handles each
    accordingly.

    The function utilizes a nested `make_struct` function to create a
    dataclass instance dynamically, which allows for flexible handling of
    the returned data structure. Additionally, it uses an `is_url` helper
    function to check if the input is a recognized URL.

    Args:
        path (pathlib.Path | str):
            The file path or URL from which the text content should be read.
        beginchar (int, optional):
            The starting index of the character range in the text content to be
            extracted. Defaults to 0.
        endchar (int, optional):
            The ending index of the character range in the text content to be
            extracted. Defaults to -1, which indicates no character range and means
            the entire text will be used.

    Returns:
        dataclass:
            An instance of the 'Result' dataclass with the following attributes:
            - text (str): The extracted substring from the read content, starting at `beginchar` and ending at `endchar`.
            - path (str): The resolved file path or URL from which the text was read.
            - beginchar (int): The starting index of the character range that was extracted.
            - endchar (int): The ending index of the character range that was extracted.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct
    import re

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
    text = "\n\n".join(
        map(lambda x: x.text if hasattr(x, "text") else str(x), elements)
    )

    # Special condition to replace the text processed by unstructured into the original
    # format.
    if key == "filename":
        try:
            raw_text = A_GIS.File.read(file=path)
            raw_stext = re.sub("\\s+", " ", raw_text).strip()
            if raw_stext.isprintable():
                stext = re.sub("\\s+", " ", text).strip()
                if raw_stext == stext:
                    text = raw_text
        except BaseException:
            pass

    # Return relevant info a struct. We transform the path to a string to make sure
    # the struct can be transformed to a dict or JSON easily.
    return A_GIS.Code.make_struct(
        text=text[beginchar:endchar],
        path=str(path),
        beginchar=beginchar,
        endchar=endchar,
    )
