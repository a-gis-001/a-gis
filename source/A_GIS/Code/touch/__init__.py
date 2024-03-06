def touch(*, path: type["pathlib.Path"]):
    import pathlib
    import A_GIS.File.touch

    # Determine the file.
    touch_path = pathlib.Path(path)
    if not path.suffix:
        touch_path /= "__init__.py"

    return A_GIS.File.touch(path=touch_path)
