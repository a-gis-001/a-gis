def to_path(*, name: str):
    """Return a path from a name, e.g. A_GIS.Code.to_path -> /path/to/A_GIS/Code/to_path."""
    import os
    import pathlib
    import A_GIS.Code.find_root

    # Get the root directory e.g. /path/to/A_GIS.
    root = A_GIS.Code.find_root(path=pathlib.Path(__file__))

    # Concatenate the parent of the root, e.g. /path/to, with the remainder
    # A_GIS.
    child = pathlib.Path(os.path.join(*name.split(".")))
    return root.parent / child
