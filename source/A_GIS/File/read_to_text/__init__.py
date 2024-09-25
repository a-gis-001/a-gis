import pathlib

def read_to_text(*, path: str, beginchar=None, endchar=None):
    """Read and partitions file or URL text using unstructured.

    This function reads the contents of a file or URL provided by the
    `path` argument and processes it with the
    `unstructured.partition.auto` function to extract structured
    elements. It then returns these elements along with the original
    path and optional start and end indices for slicing the text
    content. If the original text content is found to be identical to
    the processed content, it returns the raw text instead.

    Args:
        path (pathlib.Path | str):
            The file path or URL from which to read the text content.
            This can be a `pathlib.Path` object or a string.
        beginchar (int, optional):
            The zero-based starting index for slicing the processed text
            content. If omitted, the entire processed text is returned.
        endchar (int, optional):
            The zero-based ending index for slicing the processed text
            content. If omitted or set to `None`, no end index is
            applied, and the text will be sliced up to but not including
            this index.

    Returns:
        dataclass:
            With the following attributes

            - text (str): The extracted and partitioned text content
              from `0` to `endchar`. If `beginchar` is specified, it
              will slice from `beginchar` to `endchar`.
            - path (str): The file path or URL as a string.
            - beginchar (int | None, optional): The starting index for
              slicing the text content. It can be either an integer or
              `None`.
            - endchar (int | None, optional): The ending index for
              slicing the text content. It can be either an integer or
              `None`.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct
    import re

    # Decide whether we have a URL or a filename to call the unstructured
    # partition function with the right key.
    if A_GIS.File.is_url(name=path):
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
