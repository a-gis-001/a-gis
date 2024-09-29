def touch(*, path: type["pathlib.Path"], content_if_empty: str = ""):
    """
    Touch creates the file at the given path if it doesn't exist.

    If the directories in the path do not exist, they will be created as well.

    Args:
        path (pathlib.Path): The path to the file that you want to touch.

    Returns:
        pathlib.Path: The path of the file that was touched or created.

    Example:
        >>> import pathlib
        >>> import A_GIS.File.touch
        >>> path = A_GIS.File.touch(path=pathlib.Path("test_file"))

    """
    import A_GIS.File.read
    import A_GIS.File.write
    import pathlib

    # Create directories and create the file.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

    # Only read the file if we would replace empty content.
    if content_if_empty != "":
        content = A_GIS.File.read(file=path)
        if content.strip() == "":
            A_GIS.File.write(content=content_if_empty, file=path)

    # Update modification time.
    pathlib.Path(path).touch()

    # Return the path.
    return path
