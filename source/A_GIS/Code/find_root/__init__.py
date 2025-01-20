def find_root(
    *, path: type["pathlib.Path"], throw_if_not_found: bool = False
) -> type["pathlib.Path"]:
    """Find the root directory of a Python package"""
    import pathlib

    root = None

    # Make sure we are inside a package.
    input_path = pathlib.Path(path).resolve()
    if (input_path.parent / "__init__.py").exists() or (
        input_path / "__init__.py"
    ).exists():
        # Walk up the directory tree until the parent directory does not have
        # __init__.py.
        system_root = input_path.root
        root = input_path
        while root != system_root:
            if not (root.parent / "__init__.py").exists():
                break
            root = root.parent

    if throw_if_not_found and root is None:
        raise ValueError(f"Cannot find package root for path={path}")

    return root
