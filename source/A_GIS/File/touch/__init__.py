def touch(*, path: type["pathlib.Path"]):
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
    # Create directories and create the file.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

    # Return the path.
    return path
