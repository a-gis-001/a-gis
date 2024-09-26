def classify(*, directory: str):
    """Classify a directory based on specific marker files.

    This function examines a provided directory path and determines
    whether it is a leaf, branch, or root node in a file system
    structure by looking for the existence of specially named marker
    files within that directory. It returns a structured object
    containing information about the directory's classification, its
    existence status, and associated metadata.

    Args:
        directory (str):
            The path to the directory to be classified. This is resolved
            to an absolute path using `pathlib.Path.resolve()`.

    Returns:
        dataclass:
            An instance of a data class with the following attributes:

            - directory (str): The absolute path string of the
              directory.
            - exists (bool): A boolean indicating whether the
              directory exists.
            - root (A_GIS.File.Node, optional): An instance of
              `A_GIS.File.Node` if a root marker file is found,
              otherwise None.
            - result (str or None): The classification of the
              directory ('leaf', 'branch', 'root') if an appropriate
              marker file is found; otherwise None.
    """
    import pathlib
    import A_GIS.File.Node.get_root
    import A_GIS.Code.make_struct

    directory = pathlib.Path(directory).resolve()
    exists = directory.exists()
    result = None
    root = None
    if exists:
        root = A_GIS.File.Node.get_root(path=str(directory)).root
        if root:
            if (directory / "_leaf.node.md").exists():
                result = "leaf"
            elif (directory / "_branch.node.md").exists():
                result = "branch"
            elif (directory / "_root.node.md").exists():
                result = "root"
            elif directory.is_relative_to(root):
                result = "auxiliary"

    return A_GIS.Code.make_struct(
        directory=str(directory), exists=exists, root=root, result=result
    )
