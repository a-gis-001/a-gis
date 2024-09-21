import pathlib

def read_to_text(*, path: pathlib.Path | str):
    """Read a file or URL, partitions content, and returns formatted plain text with double newlines separating sections.

    This function reads the contents of a given file path or URL and returns
    it as a plain text string, formatted with double newlines between
    sections for readability. It leverages the `unstructured.partition.auto`
    utility to automatically partition the content into sections based on
    the provided key (filename or url).

    Args:
        path (type["pathlib.Path"] | str):
            The file system path to a local file or a URL from which to read the
            content.

    Returns:
        str:
            A string containing the plain text content of the file or the content retrieved from the URL, with double newlines between sections for visual separation. If no content is found, an empty string is returned.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct

    if not isinstance(path, pathlib.Path) or A_GIS.File.is_url(name=str(path)):
        key = "url"
    else:
        key = "filename"

    elements = unstructured.partition.auto.partition(**{key: str(path)})

    return A_GIS.Code.make_struct(text="\n\n".join(map(str, elements)))
