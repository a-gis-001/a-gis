def generate(*, description: str = "", **kwargs):
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.distill
    import A_GIS.Code.reformat
    import A_GIS.Code.extract_python

    # Create the system prompt.
    system = f"""
Given a Python function, generate and return a high-quality set of pytests.

Here is an example.

### Instruction:

name:
    A_GIS.File.Directory.init

code:
    def init(*, path: str = None, scoped_delete: bool = False):
        class _TempDir:
            def __init__(self, path: str = None, scoped_delete: bool = False):
                self.scoped_delete = scoped_delete
                self.path = path if path else tempfile.mkdtemp()

                if path and not os.path.exists(self.path):
                    os.makedirs(self.path)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> None:
                if self.scoped_delete:
                    self._delete_dir()

            def __del__(self) -> None:
                if self.scoped_delete:
                    self._delete_dir()

            def _delete_dir(self) -> None:
                if os.path.exists(self.path):
                    shutil.rmtree(self.path)

        return _TempDir(path, scoped_delete)

### Response:

docstring:

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
    Raises:
        None

    Returns:
        TempDir: An instance of the TempDir class representing the created directory.

"""

    coder = A_GIS.Ai.Chatbot.init(
        system="""
A_GIS is repository for aritificial-intelligence driven functional code.

An A_GIS functional unit is just a function, by itself in a file, with the following guidelines.

1. All imports should be absolute and inside the function.
2. All arguments are keyword arguments with type hints. Any types needed for type hints
   beyond `import typing` the standard ones should use the runtime type checking
   of the form `type['MyType']`.
3. The function is pure, meaning it does not modify their arguments or have global parameters.
4. Each function should be short, 10 lines or less. The function body can define nested functions
   which do not count towards the 10 line limit.
5. Imports must be absolute without renames, e.g. `import matplotlib.pyplot` and NOT
   `import matplotlib.pyplot as plt` or `import matplotlib.pyplot
`.

You are the primary code developer for a new A_GIS functional unit and will
create a short concise functional unit, given a request from your manager.
Your code will be short and concise WITHOUT COMMENTS and WITHOUT EXAMPLES and contained
in a Markdown block e.g.,

```python
<your A_GIS functional unit code here>
```
""",
        **kwargs,
    )

    result = coder.chat(message=description)
    content = result["message"]["content"]

    return A_GIS.Code.extract_python(text=content)
