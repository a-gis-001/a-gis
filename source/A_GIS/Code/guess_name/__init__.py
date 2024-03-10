def guess_name(*, path: type["pathlib.Path"]):
    import A_GIS.Code.find_root

    root = A_GIS.Code.find_root(path=path).resolve()
    subdir = path.relative_to(root)
    if subdir.isfile():
        subdir = subdir.parent
    return ".".join(subdir.parts)
