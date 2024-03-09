def to_path(*, name: str):
    """Return a path from a name, e.g. A_GIS.Code.to_path -> A_GIS/Code/to_path."""
    import os
    import pathlib

    return pathlib.Path(os.path.join(*name.split(".")))
