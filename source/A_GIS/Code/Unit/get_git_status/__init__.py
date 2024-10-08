def get_git_status(*, root: str = None):
    """Retrieve Git status, including staged and modified files.

    This function examines the current directory and any parent
    directories to find the nearest Git repository root. It then
    retrieves the list of staged (about to be committed) and modified
    files within that repository. Additionally, it attempts to guess the
    name associated with each file, assuming the file is part of a
    Python codebase, by using a separate function
    `A_GIS.Code.guess_name` and determines the type of the file,
    assuming it is a Python source file, by using another separate
    function `A_GIS.Code.guess_type`. The results are returned as a
    structured object with attributes for staged files, modified files,
    staged names, and modified names, along with the root path of the
    Git repository.

    Args:
        root (str, optional):
            The path to start searching for the nearest Git repository
            from. If None, the current working directory is used.

    Returns:
        A_GIS.Code.make_struct:
            With the following attributes

            - staged_files (list of str): A list of file paths that
              are staged for commit.
            - modified_files (list of str): A list of file paths that
              have been modified.
            - staged_names (list of str): A list of names associated
              with the staged files.
            - modified_names (list of str): A list of names associated
              with the modified files.
            - _root (str): The absolute path to the root directory of
              the Git repository.
    """
    import git
    import os
    import A_GIS.Code.make_struct
    import A_GIS.Code.find_root
    import A_GIS.Code.guess_name
    import pathlib

    root = pathlib.Path(root)
    git_root = root
    while not (git_root / ".git").exists():
        git_root = git_root.parent
        if git_root == git_root.parent:
            break

    # Open an existing repository
    repo = git.Repo(str(git_root))

    # Get staged files
    staged_files = [item.a_path for item in repo.index.diff("HEAD")]

    # Get modified files
    modified_files = [item.a_path for item in repo.index.diff(None)]

    def get_names(*, paths):
        names = []
        for path in paths:
            try:
                mod_path = pathlib.Path(path)
                name = A_GIS.Code.guess_name(path=mod_path.parent)
                unit_type = A_GIS.Code.guess_type(file=mod_path)
                if unit_type == "function":
                    names.append(name)
            except BaseException:
                pass
        return list(set(names))

    return A_GIS.Code.make_struct(
        staged_files=staged_files,
        modified_files=modified_files,
        staged_names=get_names(paths=staged_files),
        modified_names=get_names(paths=modified_files),
        _root=str(root),
    )
