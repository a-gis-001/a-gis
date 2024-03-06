def touch(*, path: type["pathlib.Path"]):
    import pathlib

    # Create directories and create the file.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

    # Return the path.
    return path
