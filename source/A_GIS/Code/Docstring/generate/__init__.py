import A_GIS.Log.track_function

@A_GIS.Log.track_function
def generate(
    *,
    name: str,
    code: str,
    model="wizardlm2:7b",
    temperature=0.5,
    num_ctx=10000,
    num_predict=2000,
    mirostat=2,
    reformat: bool = False,
    __tracking_hash=None,
) -> type["A_GIS.Code.Docstring._Docstring"]:
    """Generate docstring for code using AI model.

    The generated docstring is put into the Docstring object format.

    Args:
        name (str):
            The name of the function for which to generate the docstring.
        code (str):
            The Python code snippet for which to generate the docstring.
        model (str, optional):
            The AI model to use for generating the docstring. Defaults to 'deepseek-
            coder:33b'.
        temperature (float, optional):
            The temperature parameter for controlling randomness in the AI's
            response. Defaults to 0.5.
        num_ctx (int, optional):
            The number of context tokens to use when generating the docstring.
            Defaults to 10000.
        num_predict (int, optional):
            The maximum number of predicted tokens to generate in the AI's response.
            Defaults to 1000.
        mirostat (int, optional):
            The mirostat mode parameter for controlling how the AI generates its
            responses. Defaults to 2.
        reformat (bool, optional):
            If True, reformats the generated docstring to follow standard Python
            formatting rules. Defaults to False.
        __tracking_hash (str, optional):
            An internal tracking hash for tracking function execution. Defaults to
            None.

    Returns:
        str:
            generated Docstring object.
    """

    import ollama
    import A_GIS.Text.add_indent
    import A_GIS.Code.Docstring.clean
    import A_GIS.Text.get_after_tag
    import A_GIS.Text.get_before_tag
    import A_GIS.Code.Docstring.init
    import A_GIS.Code.Docstring.fix_short_description
    import A_GIS.Code.Docstring.reformat

    # Create the system prompt.
    system = f'''
Given a Python function, generate and return a high-quality docstring
following the Google docstring rules. Include the following elements.

    1. A one line summary at the beginning, less than 64 characters.
    2. Describe the capability in more detail including requirements.
    3. Arguments with full type specifications.
    4. The return value and type.

REPLY WITH ONLY THE DOCSTRING, WITHOUT TRIPLE QUOTES OR BACKTICKS!

Here is an example.

## Code

    def make_directory(*, path: str = None, scoped_delete: bool = False):
        """Replace with docstring for A_GIS.File.make_directory"""
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

## Docstring

    Creates an optionally scoped directory object.

    This function returns an instance of the nested class `TempDir`. This class
    provides functionality to create a temporary directory that can be set to
    self-delete when the object is no longer in use, based on the `scoped_delete` flag.

    Args:
        path (str, optional):
            The path where the directory should be created. If None,
            a temporary directory is created using the `tempfile` module.
        scoped_delete (bool, optional):
            If True, the created directory will be deleted
            when the TempDir object is destroyed or when exiting a context manager block.

    Returns:
        TempDir:
            An instance of the TempDir class representing the created directory.

'''

    code = A_GIS.Code.replace_docstring(
        code=code, docstring=f"Replace with docstring for {name}"
    )
    indented_code = A_GIS.Text.add_indent(text=code)
    user = f"## Code\n    {indented_code}\n"

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
    text = response["message"]["content"]
    logging.info(f"raw_output={text}")

    text = A_GIS.Text.get_after_tag(text=text, tag="## Docstring")

    # Return the content after cleaning the text. We do some extra checks
    # here to make sure we didnt' remove too much and if so we return the
    # original.
    clean = A_GIS.Code.Docstring.clean(docstring=text)
    if float(len(clean)) / float(len(text)) >= 0.8:
        text = clean

    # Three fix-up operations.
    docstring = A_GIS.Code.Docstring.init(text=text, reference_code=code)
    docstring = A_GIS.Code.Docstring.fix_short_description(
        docstring=docstring, model=model
    )
    if reformat:
        docstring = A_GIS.Code.Docstring.reformat(docstring=docstring)

    return docstring
