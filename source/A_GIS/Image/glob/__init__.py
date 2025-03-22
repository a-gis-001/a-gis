def glob(
    *,
    paths: "typing.Union[str, pathlib.Path, typing.List[typing.Union[str, pathlib.Path]]]",
    patterns: "typing.Union[str, typing.List[str]]" = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.bmp",
        "*.tiff",
        "*.webp",
    ],
    recursive: bool = True,
    ignore_patterns: "typing.Optional[typing.List[str]]" = None,
):
    """Recursively glob image files and directories into a flat list structure.

    Args:
        paths: Path or list of paths to search in
        patterns: Glob pattern or list of patterns to match. Defaults to common image formats
        recursive: Whether to search recursively
        ignore_patterns: List of patterns to ignore

    Returns:
        List of matching image file paths
    """
    import A_GIS.File.glob
    import A_GIS.Image.open
    import A_GIS.Code.make_struct
    import pathlib
    import typing

    # Get all matching image files
    file_result = A_GIS.File.glob.glob(
        paths=paths,
        patterns=patterns,
        recursive=recursive,
        ignore_patterns=ignore_patterns,
    )

    # Open all images
    images = [A_GIS.Image.open(path=file) for file in file_result.files]

    return A_GIS.Code.make_struct(
        images=images,
        files=file_result.files,
        _patterns=patterns,
        _ignore_patterns=(
            ignore_patterns if ignore_patterns is not None else []
        ),
    )
