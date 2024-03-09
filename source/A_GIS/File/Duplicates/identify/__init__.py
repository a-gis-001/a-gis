import typing

def identify(
    *, directory: type["pathlib.Path"], recurse: bool = False
) -> typing.Dict[str, typing.List["pathlib.Path"]]:
    """
    Identify duplicate files in the specified directory, with an option to recurse through subdirectories.

    This function computes the SHA-256 hash for each file in the specified directory. Files with the same hash are
    identified as duplicates. The function returns a dictionary where each key is a file hash, and the value is a list
    of file paths considered duplicates for that hash.

    Args:
        directory (pathlib.Path): The path to the directory from which to identify duplicates.
        recurse (bool): Whether to also search through subdirectories. Defaults to False.

    Returns:
        Dict[str, List[pathlib.Path]]: A dictionary mapping file hashes to lists of file paths that are duplicates.
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
            hash = A_GIS.File.hash(file)
            if hash in seen_hashes:
                if hash not in duplicates:
                    duplicates[hash] = [seen_hashes[hash]]
                duplicates[hash].append(file)
            else:
                seen_hashes[hash] = file

    return duplicates
