import A_GIS.Log.track_function

@A_GIS.Log.track_function
def rate(
    *,
    name: str,
    code: str,
    model="deepseek-coder:33b",
    temperature=0.5,
    num_ctx=10000,
    num_predict=5000,
    mirostat=2,
    __tracking_hash=None,
) -> str:
    """Generate a docstring for code using AI

    Details
    """
    import ollama
    import A_GIS.Text.add_indent
    import A_GIS.Code.Docstring.clean

    # Create the system prompt.
    system = f"""
You are an expert Python programmer.

You will be given a function and you should rate the docstring from 1-10 according to the following:

    1. A one line summary at the beginning, less than 80 characters.
    2. A block describing the detailed capability.
    3. A list of requirements under the heading Requirements:
    4. The arguments under a heading Args: using Google type specifications.
    5. The exceptions under the heading Raises:
    6. The return value under the heading Returns:

Guidelines for the rating:

    1/10 - docstring absent or does not meet any criteria
    3/10 - meets some criteria barely
    5/10 - meets all criteria barely
    7/10 - meets all criteria minimally and is well-written
    9/10 - meets all criteria fully and is extremely well-written
   10/10 - perfect :)

"""

    user = f"""
Give your numeric rating for the following function's docstring as X/10,
followed by detailed reasons for your rating framed as suggestions for
how to improve to get a 10/10.

{code}
"""

    print(user)
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
    rating = response["message"]["content"]
    return rating
