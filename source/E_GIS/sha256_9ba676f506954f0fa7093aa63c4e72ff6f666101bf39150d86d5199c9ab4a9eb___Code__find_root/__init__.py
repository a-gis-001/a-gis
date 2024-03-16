def sha256_9ba676f506954f0fa7093aa63c4e72ff6f666101bf39150d86d5199c9ab4a9eb___Code__find_root(
    *, path: type["pathlib.Path"], throw_if_not_found: bool = False
) -> type["pathlib.Path"]:
    import pathlib
    root = None
    input_path = pathlib.Path(path).resolve()
    if (
        input_path.name == "__init__.py"
        or (input_path / "__init__.py").exists()
    ):
        system_root = input_path.root
        root = input_path
        while root != system_root:
            if not (root.parent / "__init__.py").exists():
                break
            root = root.parent
    if throw_if_not_found and root is None:
        raise ValueError(f"Cannot find package root for path={path}")
    return root
