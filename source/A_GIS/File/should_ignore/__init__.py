def should_ignore(
    *,
    ignore_dirs: list = [],
    ignore_subdirs: list = [],
    only_extensions: list = [],
    ignore_dot_files: bool = True,
    ignore_tilde_files: bool = True,
    logger=None,
):
    """Returns a function that filters out file paths.

    The `should_ignore` function constructs an instance of the nested class
    `_ShouldIgnore`, which is a callable object that evaluates whether a
    given file path should be excluded from consideration based on user-
    defined criteria. This includes the ability to ignore files within
    certain directories, specific subdirectories, or only considering files
    with specified extensions, as well as respecting hidden files unless
    explicitly set not to.

    Args:
        ignore_dirs (List[str], optional):
            A list of directory paths that should be ignored when monitoring file
            changes.
        ignore_subdirs (List[str], optional):
            A list of subdirectory names that should be ignored when they appear
            within a path.
        only_extensions (Optional[List[str]]]:
            A list of file extensions for which the file will only be considered if
            it matches one of these extensions. If `None`, no filtering by file
            extension is performed.
        ignore_dot_files (bool, optional):
            If True, hidden files and directories (those starting with '.') will be
            ignored.
        logger (Optional[logging.Logger], optional):
            A logging.Logger instance to log debug messages when a path is ignored.

    Returns:
        Callable:
            A callable object that takes a single argument, `path`, and returns a
            boolean value indicating whether the file path should be ignored or not.
    """

    class _Should_Ignore:
        def __init__(self):
            self.ignore_dirs = ignore_dirs
            self.ignore_subdirs = ignore_subdirs
            self.only_extensions = only_extensions
            self.ignore_dot_files = ignore_dot_files
            self.logger = logger

        def __call__(self, *, path):
            import os

            """Helper function to determine if a file should be ignored."""
            # Ignore file changes inside specific directories or files starting
            # with "."
            if self.ignore_dot_files and any(
                part.startswith(".") for part in path.split(os.sep)
            ):
                if self.logger:
                    self.logger.debug(
                        f"Ignored hidden file or directory: {path}"
                    )
                return True

            # Ignore files that start with tilde.
            if self.ignore_dot_files and path.split(os.sep)[-1].startswith(
                "~"
            ):
                if self.logger:
                    self.logger.debug(f"Ignored file starting with ~: {path}")
                return True

            # Ignore file changes inside specific directories
            for ignored_dir in self.ignore_dirs:
                if path.startswith(os.path.abspath(ignored_dir)):
                    if self.logger:
                        self.logger.debug(f"Ignored change in: {path}")
                    return True

            # Ignore file changes inside specific named subdirectories
            dirs = set(path.split(os.sep)[:-2])
            for ignored_subdir in self.ignore_subdirs:
                if ignored_subdir in dirs:
                    if self.logger:
                        self.logger.debug(
                            f"Ignored subdir {ignored_subdir} change in: {path}"
                        )
                    return True

            # Only consider certain extensions.
            if self.only_extensions:
                ext = os.path.splitext(path)[1]
                if not ext in self.only_extensions:
                    if self.logger:
                        self.logger.debug(
                            f"Ignored because not in extension list: {path}"
                        )
                    return True

            return False

    return _Should_Ignore()
