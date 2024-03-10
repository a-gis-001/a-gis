def touch(*, name: str):
    """Touch an A_GIS code functional unit by name or path

    Note this is intended to be used within A_GIS to easily create
    new functional units.
    """

    import pathlib
    import A_GIS.File.touch

    if "." in name:
        path = A_GIS.Code.Unit.Name.to_path(name=name) / "__init__.py"
    else:
        path = pathlib.Path(name).resolve()
        if not path.suffix:
            touch_path /= "__init__.py"

    return A_GIS.File.touch(path=path)
