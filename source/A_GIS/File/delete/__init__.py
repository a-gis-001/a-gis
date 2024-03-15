def delete(file_path):
    """
    Deletes the specified file from the filesystem.

    Parameters:
    - file_path (str | pathlib.Path): The path to the file to be deleted.

    Returns:
    None
    """
    import os

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        raise FileNotFoundError(f"No such file: {file_path}")
