def recurse(
    *,
    path: type["pathlib.Path"],
    ignore_list: set[str] = {"tests"},
    _root0: type["pathlib.Path"] = None,
) -> dict:
    """Build a package tree by recursively traversing a directory.

    This function recursively explores a given directory and constructs
    a dictionary representing the directory's package structure. It
    ignores specified directories and files starting with double
    underscores (`__`). For each directory, it checks for an
    `__init__.py` file to determine if it is a package. If found, it
    further recurses into that directory to build its sub-structure.

    Args:
        path (pathlib.Path):
            The root directory path to start the recursion.
        ignore_list (set[str], optional):
            A set of directory names to be ignored during the traversal.
            Defaults to `{"tests"}`.
        _root0 (pathlib.Path, optional):
            The initial root path used internally for recursive calls.
            Defaults to `None`.

    Returns:
        dict:
            A dictionary representing the package structure with
            directory and file information.
    """
    import A_GIS.File.read
    import A_GIS.Code.Tree.get
    import pathlib

    # Quick return if we have asked for a file instead.
    if path.is_file():
        code = A_GIS.File.read(file=path)
        return A_GIS.Code.Tree.get(code=code)

    if _root0 is None:
        # Create entries list which is just the root directory/file.
        _root0 = path
        entries = [_root0]
    else:
        # If we are here from recursion, then we look at everything at this
        # path.
        entries = list(path.iterdir())

    pkg_tree = {}
    for entry in entries:
        if entry.name in ignore_list or entry.name.startswith("__"):
            continue
        if entry.is_dir():
            pkg_file = pathlib.Path(entry) / "__init__.py"
            if pkg_file.exists():
                # Get the tree to test if a package.
                tree = A_GIS.Code.Tree.get(code=A_GIS.File.read(file=pkg_file))
                if tree == {}:
                    # It is a package.
                    tree[entry.name] = recurse(
                        path=pathlib.Path(entry), _root0=_root0
                    )
                    tree[entry.name]["_type"] = "package"
                # Add file annotations.
                for x in tree:
                    if x.startswith("_"):
                        continue
                    tree[x]["_file"] = str(pkg_file)
                pkg_tree.update(**tree)

    return pkg_tree
