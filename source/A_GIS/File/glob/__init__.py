def glob(*, paths, glob_args):
    """Recursively glob files and directories in one flat list."""
    import pathlib
    file_names = []
    for path0 in paths:
        path = pathlib.Path(path0)
        if path.is_file():
            file_names.append(path)
        else:
            for glob_arg in glob_args:
                file_names.extend(list(path.glob(glob_arg)))
    return file_names
