def generate(
    *,
    name: str,
    request: str = None,
    background: str = None,
    model="qwen2.5:14b",
):
    """Generate a report for an A_GIS functional unit example.

    This function `generate` is designed to create a structured report
    containing a summary of the process, full listing of the specified
    function, and an example usage of that function. It also handles
    cases where the requested functional unit does not exist and
    provides an appropriate error message.

    The function takes four parameters:

    - `name` (str): The name of the A_GIS functional unit for which
      the example is to be generated.
    - `request` (str, optional): An optional specific request for the
      type of usage example desired. If None or an empty string, a
      default request will be used.
    - `background` (str, optional): Optional context or description
      that precedes the example usage.
    - `model` (str, optional): The AI model to use when generating the
      example. Defaults to "qwen2.5:14b".

    The function returns an instance of `dataclass` containing the
    following attributes:

    - `_name` (str): The name of the A_GIS functional unit.
    - `_request` (str): The specific request for the example usage. If
      not provided, a default request is used.
    - `_background` (str): Any additional context or description
      provided by the user. If not provided, it defaults to an empty
      string.
    - `_model` (str): The AI model used for generating the example.
      Defaults to "qwen2.5:14b".
    - `prompt` (str): The prompt that was sent to the AI chatbot,
      including any user-provided background and request.
    - `system` (str): The output from the AI chatbot, which includes
      the generated example usage.
    - `error` (Optional[str]): An error message indicating that the
      specified functional unit does not exist. This field is optional
      and only present if an error occurs.

    Returns:
        dataclass:
            With the following attributes

            - _name (str): The name of the A_GIS functional unit.
            - _request (str): The specific request for the example
              usage.
            - _background (str): Any additional context or description
              provided by the user.
            - _model (str): The AI model used for generating the
              example.
            - prompt (str): The prompt that was sent to the AI
              chatbot.
            - system (str): The output from the AI chatbot, which
              includes the generated example usage.
            - error (Optional[str]): An error message indicating that
              the specified functional unit does not exist.
    """
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.Code.make_struct
    import textwrap

    system = f"""
    You are an AI that helps users use the A_GIS codebase. They will ask you how to use a certain
    function.

    Emulate what you see in the A_GIS codebase when you respond to the user. This means, for example,
    NEVER using relative or 'as' imports like `import matplotlib.pyplot as plt`. A_GIS enforces a
    strict standard to always have absolute imports of individual functions within other functions.

    RIGHT:
        import A_GIS.Code.Unit.read
    WRONG:
        from A_GIS.Code.Unit import read
        import A_GIS.Code.Unit as unit

    You will proceed with these steps.
    1. You will use the A_GIS.Code.Unit.read tool to read the function documentation.
    2. You may also need to read functions which are referenced.
    3. You will use this documentation to create a simple but comprehensive example focusing on the user request.

    You will generate output like that shown below.

    ---

    # Generating examples for [name of function]

    Your examples section should have three sections in order: Summary of process, Full listing of function, Example usage.

    ## Summary of process

    Document your process here, including strategy and progress.

    ## Full listing of function

    Show the full listing (output of A_GIS.Code.Unit.read) for the user-requested function.

    ## Example usage

    Create an example here that first imports A_GIS, i.e. `import A_GIS`. Be specific
    about arguments. Do not leave it to the user.

    """

    error = ""
    result = None
    if not A_GIS.Code.Unit.Name.to_path(
        name=name, check_exists=False
    ).exists():
        error = f"A_GIS functional unit name '{name}' does not exist."
    else:
        prompt = ""
        if background is not None:
            prompt += f"# Background\n{background}"
        if request is None or request == "":
            request = "Give a simple usage example, printing a key result."
        prompt += f"# Request\n{request}"
        prompt += f"# Generated example for {name}\n\n"

        system = textwrap.dedent(system)
        exampler = A_GIS.Ai.Chatbot.init(
            system=system,
            num_ctx=50000,
            num_predict=10000,
            model=model,
            tool_names=["A_GIS.Code.Unit.read", "A_GIS.Code.list"],
        )
        prompt = textwrap.dedent(prompt)
        result = exampler.chat(message=prompt)

    return A_GIS.Code.make_struct(
        _name=name,
        _request=request,
        _background=background,
        _model=model,
        prompt=prompt,
        system=system,
        error=error,
        result=result,
    )
