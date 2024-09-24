def read(*, file: type["pathlib.Path"], binary: bool = False):
    """Read a file's contents as text or binary data.

    This function opens and reads the contents of a specified file in
    either text (default) or binary mode based on the `binary` flag. It
    is important to specify the correct mode to handle files with
    special encoding or files that contain binary data.

    Args:
        file (pathlib.Path, optional):
            The path to the file to be read. If None, a default file
            path should be used.
        binary (bool, optional):
            A flag indicating whether to open the file in binary mode
            ('rb', 'wb') or text mode ('r', 'w'). Defaults to False for
            text mode.

    Returns:
        str or bytes:
            The contents of the file read into memory. If
            `binary` is True, the content will be returned as bytes;
            otherwise, it will be returned as a string.
    """

    mode = "r"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        return f.read()
