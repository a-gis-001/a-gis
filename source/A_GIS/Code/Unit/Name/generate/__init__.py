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
    import textwrap
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
Brainstorm at least 10 names for the following function:
{description}
    """
    )

    x = chatbot.chat(
        message=textwrap.dedent(
            """
        Now emit in JSON a list of at least 5 names, ranked in order of quality with
        the first being the most fitting name according to the rules. Prefer generic to specific
        categories for submodules. Avoid duplicating words in the hierarchy.
         The JSON should be a simple list:
        {
            "names": ["A_GIS.X.y", "A_GIS.U.V.w"]
        }
        """
        ),
        format="json",
    )

    # Parse out the content and return a result
    content = x.response["message"]["content"]

    import json

    error = ""
    names = []
    matches = None
    try:
        matches = json.loads(content)["names"]
        for match in matches:
            try:
                # Attempt to fix the name (you can customize error handling in
                # the fix method as well)
                name = A_GIS.Code.Unit.Name.fix(name=match)
                names.append(name)
            except Exception as e:
                error += f"Error fixing name '{match}': {e}"
    except BaseException:
        names = []
        error = "Names not returned in JSON format!"

    return A_GIS.Code.make_struct(
        names=names, matches=matches, error=error, content=content
    )
