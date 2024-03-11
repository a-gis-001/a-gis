def write(*, content, file: type["pathlib.Path"], binary: bool = False):
    """Writes content to a file.

    This function writes the provided `content` to a specified `file` using Python's built-in
    `open()` function, which supports both text and binary writing based on the `binary` flag.

    Args:
            content (str or bytes): The content to write to the file. If `binary` is True, this should be a bytes object.
            file (pathlib.Path): A Path object representing the path of the file to write to.
            binary (bool, optional): If True, the file will be opened in binary mode for writing bytes. Defaults to False.

    Raises:
            None

    Returns:
            None
    """

    mode = "w"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        f.write(content)
