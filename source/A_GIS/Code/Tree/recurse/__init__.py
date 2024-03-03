import pathlib


def recurse(
    *,
    path: pathlib.Path,
    ignore_list: set[str] = {"tests"},
    _root0: pathlib.Path = None,
) -> dict:
    """
    Generate a hierarchical dictionary of code structures within a directory.

    The function traverses a directory and its subdirectories to build a tree
    of the Python code present in each. It skips directories and files specified
    in the ignore list and processes Python files and packages.

    Args:
        path: A pathlib.Path object representing the directory to traverse.
        ignore_list: An optional set of strings representing directory or file names
                     to ignore during traversal.

    Returns:
        A dictionary representing the hierarchical structure of the code.
        Directories and Python files are keys, with their respective structures
        or content as values.

    """
    import A_GIS.File.read
    import A_GIS.Code.Tree.get

    # Quick return if we have asked for a file instead.
    if path.is_file():
        code = A_GIS.File.read(file=path)
        return A_GIS.Code.Tree.get(code=code)

    if _root0 is None:
        # Create entries list which is just the root directory/file.
        _root0 = path
        entries = [_root0]
    else:
        # If we are here from recursion, then we look at everything at this path.
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
                    tree[entry.name] = recurse(path=entry, _root0=_root0)
                    tree[entry.name]["_type"] = "package"
                # Add file annotations.
                for x in tree:
                    tree[x]["_file"] = str(pkg_file)
                pkg_tree.update(**tree)

    return pkg_tree
