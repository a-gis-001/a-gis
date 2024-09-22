import pathlib

def read_to_text(*, path: pathlib.Path | str):
    """Read text from a file or URL, partitions it, and structures the content into logical sections.

    This function takes a file path or URL as input and uses the
    `unstructured.partition.auto` module to partition the text into logical
    sections. It then converts these sections into a dataclass instance
    named 'Result'. If the input is recognized as a URL, it will handle the
    retrieval of the text from the URL internally.

    Args:
        path (pathlib.Path | str):
            The file path or URL from which to read the text.

    Returns:
        dataclass: with the following attributes
            - text (str): A string representing the partitioned text content.
            - path (str): The file path or URL from which the text was read.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct

    if not isinstance(path, pathlib.Path) or A_GIS.File.is_url(name=str(path)):
        key = "url"
    else:
        key = "filename"

    elements = unstructured.partition.auto.partition(**{key: str(path)})
    text = "\n\n".join(map(str, elements))
    return A_GIS.Code.make_struct(text=text, path=str(path))
