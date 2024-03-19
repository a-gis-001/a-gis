def to_path(
    *, name: str, root: type["pathlib.Path"] = None, check_exists: bool = True
):
    """Return the path from the name of a function

    For example:
      A_GIS.Code.to_path -> /path/to/A_GIS/Code/to_path

    """
    import os
    import pathlib
    import A_GIS.Code.find_root

    # Get the root directory e.g. /path/to/A_GIS.
    if root is None:
        root = A_GIS.Code.find_root(path=pathlib.Path(__file__))

    # Concatenate the parent of the root, e.g. /path/to,
    # with the name.
    subpath = os.path.join(*name.split("."))
    path = root.parent / pathlib.Path(subpath)

    # Check that path exists before returning.
    if check_exists:
        if not path.exists():
            raise ValueError(f"Could not find path={path} from name={name}!")
    return path
