def read_to_text(*, path: str, beginchar=None, endchar=None):
    """Read a file and extract its text content.

    This function reads the contents of a file specified by `path` and
    processes it to produce a structured text output. It can handle both
    local file paths and URLs, automatically determining which method to
    use based on the input. The text content is then optionally
    partitioned using unstructured's partition function, which can be
    particularly useful for processing documents with complex layouts.
    The user can specify a range of characters to extract from the
    processed text by providing `beginchar` and `endchar` as optional
    arguments. If an error occurs during the reading or processing, it
    is caught and stored in the return value.

    Args:
        path (str):
            The file path or URL of the document to read and process.
        beginchar (int, optional):
            The starting index from which to extract text from the
            processed content. If omitted, the entire processed text is
            returned.
        endchar (int, optional):
            The ending index at which to stop extracting text from the
            processed content. If omitted or set to None, no upper limit
            is applied to the extraction.

    Returns:
        dataclass:
            With the following attributes

            - text (str): The extracted text from the processed
              content, within the specified range.
            - path (str): The file path or URL of the original
              document.
            - beginchar (int): The starting index of the extracted
              text range.
            - endchar (int): The ending index of the extracted text
              range.
            - error (str): A string containing any error that occurred
              during processing.
    """
    import unstructured.partition.auto
    import A_GIS.File.is_url
    import A_GIS.Code.make_struct
    import pathlib
    import re

    # Decide whether we have a URL or a filename to call the unstructured
    # partition function with the right key.
    key = "url" if A_GIS.File.is_url(path) else "filename"
    path = pathlib.Path(path).resolve() if key == "filename" else path

    text, error = "", ""
    try:
        # Get the elements from unstructured.
        elements = unstructured.partition.auto.partition(**{key: str(path)})

        # Join the elements with simple double newlines.
        text = "\n\n".join(
            map(lambda x: x.text if hasattr(x, "text") else str(x), elements)
        )

        # Special condition to replace the text processed by unstructured into the original
        # format.
        if key == "filename":
            raw_text = A_GIS.File.read(file=path)
            raw_stext = re.sub("\\s+", " ", raw_text).strip()
            if raw_stext.isprintable():
                stext = re.sub("\\s+", " ", text).strip()
                if raw_stext == stext:
                    text = raw_text
    except BaseException as e:
        error = str(e)

    # Do this to prevent non-unicode characters in the final text.
    text = text.encode("utf-8").decode("utf-8", errors="ignore")

    # Return relevant info a struct. We transform the path to a string to make sure
    # the struct can be transformed to a dict or JSON easily.
    return A_GIS.Code.make_struct(
        text=text[beginchar:endchar],
        path=str(path),
        beginchar=beginchar,
        endchar=endchar,
        error=error,
    )
