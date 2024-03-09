def guess_full_name(*, file: type["pathlib.Path"]):
    import A_GIS.Code.Unit.find_root

    root = A_GIS.Code.Unit.find_root(path=file)
    parts = list(file.resolve().relative_to(root.resolve().parent).parts)
    if parts[-1].startswith("__"):
        parts.pop()
    return ".".join(parts)
