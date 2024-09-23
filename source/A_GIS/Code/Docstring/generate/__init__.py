import A_GIS.Log.track_function

@A_GIS.Log.track_function
def generate(
    *,
    name: str,
    code: str,
    model="codellama:7b-python",
    temperature=0.5,
    num_ctx=15000,
    num_predict=5000,
    mirostat=2,
    reformat: bool = False,
    substitute_imports: bool = False,
    __tracking_hash=None,
) -> type["A_GIS.Code.Docstring._Docstring"]:
    """Generate high-quality Python code documentation using AI.

    The system prompt includes guidelines for creating a high-quality
    docstring, including instructions on how to structure the docstring
    and what should be included in it. The AI model is trained using
    this prompt, which ensures that the generated documentation aligns
    with established standards and best practices.

    Args:
        name (str):
            The name of the Python function or method for which a
            docstring needs to be generated. This argument serves as a
            reference point for generating a suitable system prompt.
        code (str):
            The Python code for which a docstring needs to be generated.
        model (str, optional):
            The AI model used for generating the documentation. Defaults
            to "mistral-large:latest".
        temperature (float, optional):
            A parameter controlling the randomness of the AI's
            responses. It influences the creativity and coherence of the
            generated docstring. Defaults to 0.5.
        num_ctx (int, optional):
            The number of context tokens used by the AI model for
            generating a response. Defaults to 10000.
        num_predict (int, optional):
            The maximum length of the generated docstring. Defaults to
            2000.
        mirostat (float, optional):
            A parameter controlling the decay rate of temperature during
            generation. It influences how quickly the model cools down
            and stops generating responses. Defaults to 2.
        reformat (bool, optional):
            If True, reformats the generated docstring according to
            additional rules defined by the function. If False, does not
            apply any further formatting. Defaults to False.
        substitute_imports (bool, optional):
            If True, substitutes certain import statements in the code
            with equivalent ones for improved generation of docstrings.
            If False, uses the original import statements. Defaults to
            False.
        __tracking_hash (str, optional):
            A unique hash used for tracking and debugging the function's
            execution. It can be set to any value but is typically left
            as None unless required for specific tracking purposes.

    Returns:
        `A_GIS.Code.Docstring._Docstring`:
            An instance of the `_Docstring` class, which represents a
            Python code documentation object. This object contains
            various attributes and methods related to the code's
            documentation.
    """

    import A_GIS.Ai.Chatbot.init
    import A_GIS.Text.add_indent
    import A_GIS.Code.Docstring.clean
    import A_GIS.Text.get_between_tags
    import A_GIS.Code.Docstring.init
    import A_GIS.Code.Docstring.fix_short_description
    import A_GIS.Code.Docstring.reformat
    import A_GIS.Code.Unit.substitute_imports

    # Create the system prompt.
    system = f'''
You are an expert Python documentation writer AI using Google-style Python Docstrings.

Here is an example of proper formatting.

<docstring>
Perform a sample operation that combines an integer, a float, and a string.

This function takes three parameters: an integer `x`, a float `y`, and an
optional string `z`. It performs a sample operation by combining them into
a formatted string, with `x` and `y` being added together and `z` being
appended. The result is returned as a string.

Args:
    x (int):
        An integer value that will be added to `y`.
    y (float):
        A floating-point value to add to `x`.
    z (str, optional):
        A string that will be appended to the sum of `x` and `y`.
        Defaults to "default".

Returns:
    str:
        A string that contains the sum of `x` and `y`, followed by `z`.
</docstring>

The guidelines for the docstring are:

    1. Use Google-style Python Docstrings.
    2. Include a short description sentence of less than 64 characters
       on a line by itself.
    3. Describe the capability in more detail, including requirements,
       in the long description.
    4. Should have an "Args" and "Returns" sections.
    5. Args and Returns should both have types.
    6. Do not include a "Raises" section!
    7. If the return value is created by A_GIS.Code.make_struct, put the type as
       `dataclass` and describe each of the arguments as attributes of the struct.

If a return value uses `A_GIS.Code.make_struct` then the function named arguments
are the attributes. For example, `A_GIS.Code.make_struct(text=x,path=y)` should
have a "Returns" block as follows:

<docstring>

Returns:
    dataclass:
        With the following attributes
        - text (str): A string representing the partitioned text content.
        - path (str): The file path or URL from which the text was read.

</docstring>

You will be given a Python code contained in <code> </code> tags.

You will reply with a Python docstring contained in <docstring> </docstring> tags.

For example, you could be given this code block.

<code>

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

</code>

And you would then reply with something similar to this docstring block:

<docstring>

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
    _TempDir:
        Local class with .path attribute containing the path.

</docstring>

NOTE: It is very important to determine an accurate type for the return value.
'''

    # Create the chatbot.
    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        temperature=temperature,
        num_ctx=num_ctx,
        num_predict=num_predict,
        mirostat=mirostat,
        system=system,
    )

    # Set up the user query.
    code = A_GIS.Code.replace_docstring(
        code=code, docstring=f"Replace with docstring for {name}"
    )
    if substitute_imports:
        code = A_GIS.Code.Unit.substitute_imports(code=code).code
    user = f"<code>\n{code}</code>"

    # Ask the bot and get the response.
    response = chatbot.chat(message=user).response
    text = response["message"]["content"]
    text = A_GIS.Text.get_between_tags(
        text=text, begin_tag="<docstring>", end_tag="</docstring>"
    )

    # Return the content after cleaning the text. We do some extra checks
    # here to make sure we didnt' remove too much and if so we return the
    # original.
    clean = A_GIS.Code.Docstring.clean(docstring=text)
    if float(len(clean)) / float(len(text)) >= 0.8:
        text = clean

    # Three fix-up operations.
    docstring = A_GIS.Code.Docstring.init(text=text, reference_code=code)
    docstring = A_GIS.Code.Docstring.fix_short_description(docstring=docstring)
    if reformat:
        docstring = A_GIS.Code.Docstring.reformat(docstring=docstring)

    return docstring
