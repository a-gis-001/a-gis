def guess_name(*, path: type["pathlib.Path"]):
    import A_GIS.Code.find_root
    import pathlib

    root = A_GIS.Code.find_root(path=path).resolve().parent
    subdir = pathlib.Path(path).resolve().relative_to(root)
    if subdir.is_file():
        subdir = subdir.parent
    return ".".join(subdir.parts)
