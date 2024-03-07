def open(*, path: type["pathlib.Path"], binary=False, chunk_size=1024):
    import builtins
    import A_GIS.File._Url
    import A_GIS.File.is_url

    mode = "r"
    if binary:
        mode += "b"

    if A_GIS.File.is_url(path):
        return A_GIS.File._Url(path, chunk_size=chunk_size, binary=binary)
    else:
        return builtins.open(path, mode)
