import A_GIS.Log.track_function

@A_GIS.Log.track_function
def generate(
    *,
    description: str,
    model="qwq",
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
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.make_struct

    # Create a list of examples.
    def format_examples(suggestions):
        example_list = A_GIS.catalog(
            entry_format="Function description: {description} --> Function name: {header}",
            include_args=False,
        )
        for suggestion in suggestions:
            example_list.append(
                "Function description: {description} --> Function name: {suggestion}"
            )
        examples = ""
        for e in example_list:
            if not e.startswith("None"):
                examples += "- " + e + "\n"
        return A_GIS.Text.add_indent(text=examples)

    examples = format_examples(suggestions)

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

You should think and discuss with yourself as much as necessary, but in the
end you should emit 5 ranked function names with 1. being the best function name.
Prefix your final list with FINAL LIST: in all capitals. For example:

FINAL LIST:
1. A_GIS.Code.simplify
2. A_GIS.Code.reduce
3. A_GIS.Code.optimize
4. A_GIS.Code.Unit.simplify
5. A_GIS.Code.Unit.Name.simplify
"""

    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        system=system,
        temperature=0.5,
        num_ctx=10000,
        num_predict=20000,
        mirostat=2,
    )
    x = chatbot.chat(
        message=f"""
    Generate 5 synonomous names for a function that: {description}
    Don't forget to put the final list after
    FINAL LIST:
    """
    )

    # Parse out the content and return a result
    content = x.response["message"]["content"]

    try:
        # Check if 'FINAL LIST:' exists in the content
        i = content.index("FINAL LIST:")
    except ValueError:
        print("Error: 'FINAL LIST:' not found in the content.")
        matches = []
    else:
        # If 'FINAL LIST:' is found, continue with the search
        matches = re.findall(r"(A_GIS\.[A-Za-z_\.]+)", content[i:])

    if matches:
        # Process the matches if any are found
        names = []
        for match in matches:
            try:
                # Attempt to fix the name (you can customize error handling in
                # the fix method as well)
                fixed_name = A_GIS.Code.Unit.Name.fix(name=match)
                names.append(fixed_name)
            except Exception as e:
                print(f"Error fixing name '{match}': {e}")
    else:
        print("Warning: No matches found after 'FINAL LIST:'.")
        names = []

    # Result
    print("Processed Names:", names)

    return A_GIS.Code.make_struct(
        names=names, content=content, matches=matches
    )
