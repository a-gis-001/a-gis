def glob(
    *,
    paths: "typing.Union[str, pathlib.Path, typing.List[typing.Union[str, pathlib.Path]]]",
    patterns: "typing.Union[str, typing.List[str]]" = "**/*",
    recursive: bool = True,
    ignore_patterns: "typing.Optional[typing.List[str]]" = [".*","*~"]
):
    """Recursively glob files and directories into a flat list structure.

    Args:
        paths: Single path or list of paths to glob from. Each path can be string or Path.
            All paths will be converted to absolute paths.
        patterns: Single pattern or list of patterns to match against.
            Default "**/*" matches all files recursively.
        recursive: Whether to search subdirectories recursively. Defaults to True.
        ignore_patterns: List of glob patterns to ignore. Common patterns:
            - ".*" - Hidden files and directories
            - "**/tests/**" - Test directories
            - "*/__pycache__/*" - Python cache
            - "*/node_modules/*" - Node.js modules
            - "*/.git/*" - Git directory
            - "*/.pytest_cache/*" - Pytest cache
            - "*/.mypy_cache/*" - MyPy cache
            - "*/.coverage" - Coverage data
            - "*.pyc" - Python compiled
            - "*~" - Temp files
            - "*.swp" - Vim swap files

    Returns:
        A_GIS.Code.make_struct containing:
            files: List[Path] - All matched absolute file paths
            _patterns: Glob patterns used
            _ignore_patterns: Patterns used for ignoring files
    """
    import A_GIS.Code.make_struct
    import pathlib
    import typing
    import fnmatch

    def should_ignore_path(path: pathlib.Path) -> bool:
        """Check if a path should be ignored based on patterns and settings.

        Args:
            path: Path to check

        Returns:
            bool: True if path should be ignored
        """

        # Convert simple directory names to proper glob patterns
        expanded_patterns = []
        for pattern in ignore_patterns:
            if "/" not in pattern and "*" not in pattern:
                # It's a simple directory/file name - match it anywhere in path
                expanded_patterns.append(f"**/{pattern}/**")
                expanded_patterns.append(f"**/{pattern}")  # For files
            else:
                expanded_patterns.append(pattern)

        str_path = str(path)
        return any(fnmatch.fnmatch(str_path, pattern) for pattern in expanded_patterns)

    # Normalize inputs
    if isinstance(paths, (str, pathlib.Path)):
        paths = [paths]
    if isinstance(patterns, str):
        patterns = [patterns]

    # Convert all paths to absolute Path objects
    paths = [pathlib.Path(p).resolve() for p in paths]

    files = []
    for path in paths:
        if path.is_file():
            if not should_ignore_path(path):
                files.append(path)
        else:
            for pattern in patterns:
                if recursive:
                    matched = path.rglob(pattern)
                else:
                    matched = path.glob(pattern)

                for file_path in matched:
                    # Convert each matched path to absolute
                    file_path = file_path.resolve()
                    if should_ignore_path(file_path):
                        continue
                    if file_path.is_file():
                        files.append(file_path)

    return A_GIS.Code.make_struct(
        files=[str(file) for file in sorted(files)],
        _patterns=patterns,
        _ignore_patterns=ignore_patterns if ignore_patterns is not None else []
    )
