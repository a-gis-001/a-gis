def glob(
    *,
    paths: "typing.Union[str, pathlib.Path, typing.List[typing.Union[str, pathlib.Path]]]",
    patterns: "typing.Union[str, typing.List[str]]" = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp"],
    recursive: bool = True,
    ignore_patterns: "typing.Optional[typing.List[str]]" = None
):
    """Recursively glob images into one flat list.

    Args:
        paths: Single path or list of paths to glob from. Each path can be string or Path.
            All paths will be converted to absolute paths.
        patterns: Single pattern or list of patterns to match image files.
            Defaults to common image extensions.
        recursive: Whether to search subdirectories recursively. Defaults to True.
        ignore_patterns: List of glob patterns to ignore. Common patterns:
            - ".*" - Hidden files and directories
            - "**/tests/**" - Test directories
            - "**/thumbnails/**" - Thumbnail directories
            - "**/*_thumb.*" - Thumbnail files
            - "**/temp/**" - Temporary directories

    Returns:
        A_GIS.Code.make_struct containing:
            images: List of opened image objects
            files: List[str] - All matched absolute file paths
            _patterns: Glob patterns used
            _ignore_patterns: Patterns used for ignoring files
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
        ignore_patterns=ignore_patterns
    )

    # Open all images
    images = [A_GIS.Image.open(path=file) for file in file_result.files]

    return A_GIS.Code.make_struct(
        images=images,
        files=file_result.files,
        _patterns=patterns,
        _ignore_patterns=ignore_patterns if ignore_patterns is not None else []
    )
