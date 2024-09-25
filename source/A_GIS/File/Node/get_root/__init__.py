def get_root(*, path: str):
    """Retrieve the root `.node.md` directory from a file system path.

    This function searches for the nearest ancestor directory containing
    a file named `_root.node.md` within the specified `path`. It
    traverses up the directory hierarchy until it finds this file or
    reaches the top-level directory. The search is performed by checking
    for the existence of the specific file at each level of the
    directory tree. Once the root directory is found, its path is
    returned along with the original input path.

    Args:
        path (str):
            The path for which the root `.node.md` directory is to be
            found.

    Returns:
        dataclass:
            With the following attributes

            - root (str): A string representing the path of the root
              `.node.md` directory found.
            - path (str): A string representing the original input
              path provided.
    """
    import pathlib
    import A_GIS.Code.make_struct

    current_path = pathlib.Path(path)
    root = None
    while True:
        if (current_path / "_root.node.md").exists():
            root = current_path
            break

        # Move up one directory
        parent_path = current_path.parent

        # Reached the root
        if parent_path == current_path:
            break

        # Continue
        current_path = parent_path

    return A_GIS.Code.make_struct(root=str(root), path=str(path))
