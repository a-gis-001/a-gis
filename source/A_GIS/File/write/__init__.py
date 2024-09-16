def write(*, content, file: type["pathlib.Path"], binary: bool = False):
    """Write content to a file, with an option to specify binary mode.

    This function writes the provided `content` to the specified `file`. The
    `binary` flag determines whether the write operation is performed in
    binary mode or text mode. If `binary` is set to `True`, the file will be
    opened in binary write mode; otherwise, it will be opened in text mode.

    Args:
        content (str):
            The data to be written to the file.
        file (pathlib.Path):
            The path object representing the file to write to.
        binary (bool, optional):
            A flag that indicates whether the write operation should be performed in
            binary mode (True) or text mode (False). Defaults to False.

    Returns:
        None:
            The function does not explicitly return a value as it performs an in-place modification of the file specified by `file`.
    """

    mode = "w"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        f.write(content)
