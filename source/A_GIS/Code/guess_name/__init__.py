def guess_name(*, path: type["pathlib.Path"]):
    """Guesses a package name for a given path based on its parent directory structure.

    The function attempts to find the root directory corresponding to the provided path,
    then calculates a package name by joining all parts of the relative path from the root's
    parent directory down to the provided path. If the provided path is a file, it will be
    used as the base for the calculation and its parent directory will be used instead.

    Args:
        path (pathlib.Path): The path to guess the package name from.

    Raises:
        ValueError: If the root corresponding to the provided path could not be found.

    Returns:
        str: A package name string created by joining parts of the relative path from the
             root's parent directory down to the provided path, separated by dots.
    """

    import A_GIS.Code.find_root
    import pathlib

    path = path.resolve()
    root = A_GIS.Code.find_root(path=path)
    if root is None:
        raise ValueError(
            f"The root corresponding to path={path} could not be found!"
        )

    root = root.resolve().parent
    if path.is_file():
        path = path.parent

    subdir = pathlib.Path(path).resolve().relative_to(root)
    return ".".join(subdir.parts)
