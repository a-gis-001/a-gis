def is_subdirectory(
    *,
    parent: type["pathlib.Path"],
    sub: type["pathlib.Path"],
    allow_same: bool = False,
) -> bool:
    """Check sub is a subdirectory of parent."""
    import pathlib

    # Resolve both paths to get absolute paths and eliminate any '..' or
    # symbolic links
    try:
        parent = parent.resolve(strict=True)
        sub = sub.resolve(strict=True)
        if allow_same and parent == sub:
            return True
        return parent in sub.parents
    except FileNotFoundError:
        return False
