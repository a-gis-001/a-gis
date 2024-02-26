def make(*, path: str = None, scoped_delete: bool = False):
    """
    Creates a directory object that may delete itself when it goes out of scope.

    This function returns an instance of the nested class `TempDir`. This class
    provides functionality to create a temporary directory that can be set to
    self-delete when the object is no longer in use, based on the `scoped_delete` flag.

    Args:
        path (str, optional): The path where the directory should be created. If None,
                              a temporary directory is created using the `tempfile` module.
        scoped_delete (bool, optional): If True, the created directory will be deleted
                                        when the TempDir object is destroyed or when
                                        exiting a context manager block.

    Returns:
        TempDir: An instance of the TempDir class representing the created directory.

    Examples:
        >>> import A_GIS.File.Directory.make
        >>> with A_GIS.File.Directory.make(scoped_delete=True) as temp_dir:
        ...     pass
    """
    import os
    import tempfile
    import shutil
    class _TempDir:
        def __init__(self, path: str = None, scoped_delete: bool = False):
            """Initializes the TempDir object."""
            self.scoped_delete = scoped_delete
            self.path = path if path else tempfile.mkdtemp()

            if path and not os.path.exists(self.path):
                os.makedirs(self.path)

        def __enter__(self):
            """Called when entering the 'with' block."""
            return self

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            """Called when exiting the 'with' block."""
            if self.scoped_delete:
                self._delete_dir()

        def __del__(self) -> None:
            """Called when the object is about to be destroyed."""
            if self.scoped_delete:
                self._delete_dir()

        def _delete_dir(self) -> None:
            """Helper method to delete the directory."""
            if os.path.exists(self.path):
                shutil.rmtree(self.path)

    return _TempDir(path, scoped_delete)
