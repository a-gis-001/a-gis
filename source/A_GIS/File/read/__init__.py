def read(*, file: type["pathlib.Path"], binary: bool = False):
    """Reads the content of a file. The function opens and reads the content from the specified file path. It can read text or binary files based on the `binary` flag. If `binary` is True, the file is opened in binary mode (i.e., 'rb'). Otherwise, it's opened in text mode (i.e., 'r').

    Args:
        file (pathlib.Path): The path to the file that should be read.
        binary (bool, optional): If True, the file is read in binary mode. Defaults to False.

    Raises:
        FileNotFoundError: If the specified `file` does not exist.
        IOError: If there's an issue opening or reading from the file.

    Returns:
        str | bytes: The content of the file as a string (if `binary` is False) or bytes object (if `binary` is True).
    """

    mode = "r"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        return f.read()
