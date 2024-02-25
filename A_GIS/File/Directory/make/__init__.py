def make(*, path=None, scoped_delete=False):
    """Creates a directory object that may delete itself when it goes out of scope."""
    import os
    import tempfile
    import shutil

    class TempDir:
        def __init__(self, path=None, scoped_delete=False):
            self.scoped_delete = scoped_delete

            if path:
                self.path = path
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
            else:
                # Create a temporary directory
                self.path = tempfile.mkdtemp()

        def __enter__(self):
            # This method is called when entering the 'with' block
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # This method is called when exiting the 'with' block
            if self.scoped_delete:
                # Delete the directory if scoped_delete is True
                shutil.rmtree(self.path)

        def __del__(self):
            # This method is called when the object is about to be destroyed
            if self.scoped_delete:
                # Delete the directory if scoped_delete is True
                if os.path.exists(self.path):
                    shutil.rmtree(self.path)

    return TempDir(path, scoped_delete)
