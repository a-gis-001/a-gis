def guess_name(*, path: type["pathlib.Path"]):
    import A_GIS.Code.find_root
    import pathlib

    root = A_GIS.Code.find_root(path=path)
    if root is None:
        raise ValueError(
            f"The root corresponding to path={path} could not be found!"
        )

    root = root.resolve().parent
    subdir = pathlib.Path(path).resolve().relative_to(root)
    if subdir.is_file():
        subdir = subdir.parent
    return ".".join(subdir.parts)
