def list_branches(*, dirname: str = ".", _root=None):
    """Retrieve branch directories within a specified directory.

    This function searches for branches by looking for a specific file,
    `_branch.node.md`, in each directory level below the specified
    `dirname`. It uses a recursive `os.walk` traversal with the
    `topdown=True` option to allow for early termination of the walk
    when a branch node is found, thus avoiding unnecessary traversal of
    subdirectories.

    The function returns a structured data object created by
    `A_GIS.Code.make_struct`, which includes the paths to the branches
    found and information about the directory structure.

    Args:
        dirname (str, optional):
            The name of the directory to start searching for branch
            nodes from. Defaults to the current working directory.
        _root (str, optional):
            An optional path that specifies the root directory relative
            to which the target directory is resolved. This is used to
            provide absolute paths in the output even if `dirname` is a
            relative path.

    Returns:
        dataclass:
            A structured data object with the following attributes:

            - branches (list of str): A list of strings representing
              the paths to branch nodes.
            - dirname (str): The name of the directory from which the
              search started.
            - _root_dir (str): The root directory, possibly absolute,
              used as a reference point for the relative paths of the
              found branches.
            - _target_dir (str): The target directory where the search
              for branch nodes was performed.
    """
    import pathlib
    import os
    import A_GIS.Code.make_struct
    import A_GIS.File.Node._get_dir_root

    target_dir, root_dir = A_GIS.File.Node._get_dir_root(
        dirname=dirname, root=_root
    )

    # Recurse through to find branches nodes. Must use top_down so that
    # we can modify dirnames and prevent recursing through unnecessary depth.
    branches = []
    for dirpath, dirnames, filenames in os.walk(str(target_dir), topdown=True):
        for filename in filenames:

            # Branch nodes by definition have this file.
            if filename.lower() == "_branch.node.md":
                branches.append(
                    str(pathlib.Path(dirpath).relative_to(root_dir))
                )

            # If we find a branch node then we don't need to go deeper so we empty
            # the dirnames.
            dirnames = []

        # Do not recurse into _ or _inbox or anything else starting with _.
        dirnames[:] = [
            dirname for dirname in dirnames if not dirname.startswith("_")
        ]

    # Return the struct to use in AI tool calling.
    return A_GIS.Code.make_struct(
        branches=branches,
        dirname=str(dirname),
        _root_dir=str(root_dir),
        _target_dir=str(target_dir),
    )
