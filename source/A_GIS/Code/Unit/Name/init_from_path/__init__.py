def init_from_path(*, path: type["pathlib.Path"]):
    """Initialize an A_GIS functional code unit from a path

    Requirements:
       - Path must exist.

    """
    import A_GIS.Code.find_root

    root = A_GIS.Code.find_root(path=path)
    parts = list(path.resolve().relative_to(root.resolve().parent).parts)
    if parts[-1].startswith("__"):
        parts.pop()
    return ".".join(parts)
