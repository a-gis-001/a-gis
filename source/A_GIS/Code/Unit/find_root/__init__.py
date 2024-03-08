def find_root(*, path: type["pathlib.Path"]) -> type["pathlib.Path"]:
    """Find the root directory of a Python package"""
    import pathlib

    # Initialize path.
    current_path = pathlib.Path(path).resolve()

    # Make sure we are inside a package.
    if not (
        current_path.name == "__init__.py"
        or (current_path / "__init__.py").exists()
    ):
        return None

    # Walk up the directory tree until the parent directory does not have
    # __init__.py.
    while current_path != current_path.root:
        if not (current_path.parent / "__init__.py").exists():
            break
        current_path = current_path.parent

    return current_path
