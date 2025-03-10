def glob(
    *,
    paths: "typing.Union[str, pathlib.Path, typing.List[typing.Union[str, pathlib.Path]]]",
    patterns: "typing.Union[str, typing.List[str]]" = "**/*",
    recursive: bool = True,
    include_hidden: bool = False,
    ignore_patterns: "typing.Optional[typing.List[str]]" = None,
    additional_ignore_patterns: "typing.Optional[typing.List[str]]" = None
) -> "A_GIS.Code.Struct":
    """Recursively glob files and directories into a flat list structure.
    
    Args:
        paths: Single path or list of paths to glob from. Each path can be string or Path.
            All paths will be converted to absolute paths.
        patterns: Single glob pattern or list of patterns to match against.
            Default "**/*" matches all files recursively.
        recursive: Whether to search subdirectories recursively. Defaults to True.
        include_hidden: Whether to include hidden files/directories. Defaults to False.
        ignore_patterns: List of glob patterns to ignore. If provided, replaces default patterns.
            Common defaults if None:
            - ".*" - Hidden files and directories
            - "*/__pycache__/*" - Python cache
            - "*/node_modules/*" - Node.js modules
            - "*/.git/*" - Git directory
        additional_ignore_patterns: List of glob patterns to ignore in addition to defaults
            or ignore_patterns if specified. Patterns can be:
            - Full paths: "path/to/ignore"
            - Directory names: "dirname" (will match any path containing this directory)
            - Glob patterns: "*.pyc", "**/tests/**"
            
    Returns:
        A_GIS.Code.Struct containing:
            files: List[Path] - All matched absolute file paths
            _paths: Original input paths converted to absolute paths
            _patterns: Original glob patterns used
            _recursive: Whether recursive search was used
            _include_hidden: Whether hidden files were included
            _ignore_patterns: All patterns used for ignoring files
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
        # Default ignore patterns if none provided
        default_ignores = [
            ".*",  # Hidden files
            "*/__pycache__/*",  # Python cache
            "*/node_modules/*",  # Node.js modules
            "*/.git/*",  # Git directory
            "*/.pytest_cache/*",  # Pytest cache
            "*/.mypy_cache/*",  # MyPy cache
            "*/.coverage",  # Coverage data
            "*.pyc",  # Python compiled
            "*~",  # Temp files
            "*.swp",  # Vim swap files
        ]
        
        # Build final list of patterns to check
        patterns_to_check = ignore_patterns if ignore_patterns is not None else default_ignores
        if additional_ignore_patterns:
            # Convert simple directory names to proper glob patterns
            expanded_patterns = []
            for pattern in additional_ignore_patterns:
                if "/" not in pattern and "*" not in pattern:
                    # It's a simple directory/file name - match it anywhere in path
                    expanded_patterns.append(f"**/{pattern}/**")
                    expanded_patterns.append(f"**/{pattern}")  # For files
                else:
                    expanded_patterns.append(pattern)
            patterns_to_check = patterns_to_check + expanded_patterns
            
        if not include_hidden:
            patterns_to_check = [".*"] + patterns_to_check
            
        str_path = str(path)
        return any(fnmatch.fnmatch(str_path, pattern) for pattern in patterns_to_check)
    
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
    
    # Combine all active ignore patterns for metadata
    final_ignore_patterns = ignore_patterns if ignore_patterns is not None else []
    if additional_ignore_patterns:
        final_ignore_patterns = final_ignore_patterns + additional_ignore_patterns
    
    return A_GIS.Code.make_struct(
        files=files,
        _paths=paths,
        _patterns=patterns,
        _recursive=recursive,
        _include_hidden=include_hidden,
        _ignore_patterns=final_ignore_patterns
    )
 