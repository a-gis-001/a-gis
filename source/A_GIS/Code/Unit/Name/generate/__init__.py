import A_GIS.Log.function

@A_GIS.Log.function
def generate(
    *,
    description: str,
    model="deepseek-coder:33b",
    temperature=0.5,
    num_ctx=10000,
    num_predict=50,
    mirostat=2,
    suggestions=[],
    __tracking_hash=None,
):
    """Generate an A_GIS functional unit name using AI."""
    import ollama
    import re
    import A_GIS.catalog
    import A_GIS.Log.append
    import A_GIS.Text.add_indent
    import A_GIS.Code.Unit.Name.fix

    # Create a list of examples.
    example_list = A_GIS.catalog(
        entry_format="Function description: {description} --> Function name: {header}",
        include_args=False,
    )
    examples = ""
    for example in example_list + suggestions:
        if not example.startswith("None"):
            examples += "- " + example + "\n"
    examples = A_GIS.Text.add_indent(text=examples)

    # Create the system prompt.
    system = f"""
You are in charge of naming a function in the A_GIS code system. A_GIS is a Python-based
repository for AI-generated code. The hierarchy should be general and not include
Python-specific naming like Pip or Python or PILLOW.

I will give you a description of the function and you will reply with the fully
qualified name of that function. A_GIS has particular rules which you should follow.

Requirements:
    1. Parts separated with '.' as in Python.
    2. First part is 'A_GIS', always.
    3. Last part is a function name and is lower case with underscores '_' allowed.
    4. Other parts are package names and are capitalized, first letter only.
    5. There are no underscores '_' in a package name.
    6. Package names are simple, generic nouns.
    7. The first word in a function name is a verb.

Here are some examples:

{examples}

Note that you should use the most pythonic synonym for a concept. For example, if
the description of the function calls for deleting, synonyms could be 'clear',
'remove', 'delete', etc., use the least ambiguous synonym for the given context.

Be careful about introducing unnecessary hierarchy for synonymous concepts.

Shorter is better but you never respond with an empty result!
"""

    user = f"Function description: {description} --> Function name: "

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
    A_GIS.Log.append(tracking_hash=__tracking_hash, response=response)

    # Parse out the content and return a result.
    content = response["message"]["content"]
    matches = re.findall(r"(A_GIS\.[A-Za-z_\.]+)", content)
    result = "" if len(matches) == 0 else matches[0]
    result = A_GIS.Code.Unit.Name.fix(name=result)
    return result
