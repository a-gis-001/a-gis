def recommend(*, query: str, model="qwen2.5:14b"):
    """Recommend AI functions based on user query.

    This function utilizes an AI model to interpret a user's query and
    recommend the most appropriate functions from the A_GIS codebase. It
    returns a structured result containing the query, the AI model used,
    the system prompt, the chatbot response, the recommended
    function(s), and additional context required to execute the
    recommendation.

    Args:
        query (str): The user's search query as a string
        model (str, optional): The specific AI model to use for the recommendation.
            Defaults to "qwen2.5:14b"

    Returns:
        Result: A dataclass with the following attributes:

            - _query: The user's search query
            - _model: The AI model used for the recommendation
            - system: The complete system prompt used for
              generating the recommendations
            - prompt: The specific chatbot prompt used to
              generate the list of functions
            - result: A nested dataclass containing the
              results from the chatbot interaction
            - function: The fully qualified name(s) of the
              recommended function(s)
            - function_prompt: The prompt used to extract the
              top recommended function from the list of
              recommendations
    """
    import textwrap
    import A_GIS.Code.make_struct
    import A_GIS.catalog
    import A_GIS.Ai.Chatbot.init

    lines = A_GIS.catalog()
    available = "\n".join(lines)

    system = f"""
    You are an AI that helps a user find the appropriate function in the A_GIS codebase according to their needs.
    A_GIS is a generic code base for AI-generated and managed code.

    You will proceed with these steps.
    1. You will choose 10 of these functions from the full list, only from public functions which do not start with an underscore!
    2. You will use the A_GIS.Code.Unit.read tool to read the function documentation and verify it meets the user's needs.
    3. If it does not meet the user's needs or you believe another function might better, you will return to step 2.
    4. You will find 3 reasonable functions to recommend to the user.
    5. For your number one recommendation, you will output the full text of the function from A_GIS.Code.Unit.read.

    # Available functions

    {available}

    ---

    # Your response

    Your response should have three sections in order: Summary of search, Top 3 functions, Full listing of top function.

    ## Summary of search

    Document your search findings here, including strategy and progress and the 10 selected functions.

    1.
    2.
    3.
    ...
    10.

    ## Top 3 functions

    This section contains a list of the 3 fully qualified function
    names in order.

    1. A_GIS.X.Y.z
    2. A_GIS.U.V.w
    3. None (could not find a third)

    If you cannot find 3 fitting functions, show None in the list.

    ## Full listing of top function

    Show the full listing (output of A_GIS.Code.Unit.read) for the top function.

    """
    system = textwrap.dedent(system)
    finder = A_GIS.Ai.Chatbot.init(
        system=system,
        num_ctx=50000,
        num_predict=10000,
        model=model,
        tool_names=["A_GIS.Code.Unit.read", "A_GIS.Code.list"],
    )

    prompt = "User query: " + query
    result = finder.chat(message=prompt)
    function_prompt = "What is the top recommended function? Reply with only the top recommended function name on a single line and no other data."

    function_result = finder.chat(message=function_prompt)
    function_name = function_result.response["message"]["content"]

    return A_GIS.Code.make_struct(
        _query=query,
        _model=model,
        system=system,
        prompt=prompt,
        result=result,
        function=function_name,
        function_prompt=function_prompt,
    )
