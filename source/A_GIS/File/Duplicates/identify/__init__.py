import typing

def identify(
    *, directory: type["pathlib.Path"], recurse: bool = False
) -> typing.Dict[str, typing.List["pathlib.Path"]]:
    """Find duplicate files within a directory.

    This function scans the specified directory and its subdirectories
    (if `recurse` is True) to find all files, computes their hashes, and
    identifies any duplicates. It returns a dictionary where each key is
    a hash of a file, and the corresponding value is a list of paths to
    files with that hash.

    Args:
        directory (pathlib.Path):
            The directory to scan for duplicate files. This is an
            instance of `pathlib.Path`.
        recurse (bool, optional):
            If True, the function will search through all subdirectories
            within the specified directory. Defaults to False, which
            means it will only consider files in the specified directory
            itself.

    Returns:
        dict[str, list[pathlib.Path]]:
            A dictionary where each key is a unique hash of a file found
            in the directory or its subdirectories. Each value is a list
            of `pathlib.Path` objects representing all files with that
            hash. An empty dictionary is returned if no duplicates are
            found.
    """
    import pathlib
    import A_GIS.File.hash

    seen_hashes = {}
    duplicates = {}

    if recurse:
        files = directory.rglob("*")
    else:
        files = directory.glob("*")

    for file in files:
        if file.is_file():
            hash = A_GIS.File.hash(file=file)
            if hash in seen_hashes:
                if hash not in duplicates:
                    duplicates[hash] = [seen_hashes[hash]]
                duplicates[hash].append(file)
            else:
                seen_hashes[hash] = file

    return duplicates
