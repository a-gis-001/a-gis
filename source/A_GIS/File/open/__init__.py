def open(*, path: type["pathlib.Path"], binary=False, chunk_size=1024):
    """Open a file or URL for reading, optionally in binary mode.

    This function opens either a local file or a remote resource specified by a URL. 
    The type of the opened object (file or URL) is determined based on whether the 
    provided path is a URL or not. If it's a URL, an instance of `A_GIS.File._Url` 
    is returned which handles reading from a URL. If it's a local file, the built-in 
    `open` function is used to open and return the file object.

    Args:
		path (pathlib.Path): The path or URL to the resource to be opened.
		binary (bool, optional): Whether to open the file in binary mode. Defaults to False.
		chunk_size (int, optional): If opening a URL, this is the size of chunks to 
		                            read from the URL at once. Defaults to 1024 bytes.

    Raises:
		None

    Returns:
		Union[builtins.open, A_GIS.File._Url]: An instance of either `A_GIS.File._Url` 
		or a built-in file object representing the opened resource.
    """

    import builtins
    import A_GIS.File._Url
    import A_GIS.File.is_url

    mode = "r"
    if binary:
        mode += "b"

    if A_GIS.File.is_url(path):
        return A_GIS.File._Url(path, chunk_size=chunk_size, binary=binary)
    else:
        return builtins.open(path, mode)
