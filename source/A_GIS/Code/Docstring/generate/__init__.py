import A_GIS.Log.track_function

@A_GIS.Log.track_function
def generate(
    *,
    name: str,
    code: str,
    model="deepseek-coder:33b",
    temperature=0.5,
    num_ctx=10000,
    num_predict=1000,
    mirostat=2,
) -> str:
    """Generate a docstring for code using AI

    Details
    """
    import ollama
    import A_GIS.Text.add_indent
    import A_GIS.Code.Docstring.clean

    # Create the system prompt.
    system = f"""
Given a Python function, generate and return a high-quality docstring
with the following elements

    1. A one line summary at the beginning, less than 80 characters.
    2. Describe the capability in more detail.
    3. List the requirements.
    4. List the arguments with full type specifications.
    5. List what the function raises.
    6. List the return value.

REPLY WITH ONLY THE DOCSTRING, WITHOUT TRIPLE QUOTES OR BACKTICKS!

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

    indented_code = A_GIS.Text.add_indent(text=code)
    user = f"name:\n    {name}code:\n{indented_code}\n"

    import logging

    logging.info("raw_input={user}")

    # Set up the messages with system and user content. Assistant content does
    # not seem to work so well.
    messages = [
        {
            "role": "system",
            "content": system,
        },
        {
            "role": "user",
            "content": user,
        },
    ]

    # Retrieve the response.
    response = ollama.chat(
        model=model,
        messages=messages,
        options=ollama.Options(
            temperature=temperature,
            num_ctx=num_ctx,
            num_predict=num_predict,
            mirostat=mirostat,
        ),
    )
    docstring = response["message"]["content"]
    logging.info(f"raw_output={docstring}")

    # Fix up the reply including the docstring:
    tag = "docstring:"
    t = docstring.find(tag)
    if t >= 0:
        docstring = docstring[t + len(tag) :]
    tag = "### Instruction:"
    t = docstring.find(tag)
    if t >= 0:
        docstring = docstring[:t]

    # Return the content after cleaning the docstring. We do some extra checks
    # here to make sure we didnt' remove too much and if so we return the
    # original.
    clean_docstring = A_GIS.Code.Docstring.clean(docstring=docstring)
    if float(len(clean_docstring)) / float(len(docstring)) >= 0.8:
        docstring = clean_docstring
    return docstring
