def fix_short_description(
    *,
    docstring: type["A_GIS.Code.Docstring._Docstring"],
    force_ai=False,
) -> str:
    """Fix the short description in the docstring.

    The short description is the first line of the docstring and in
    many cases is printed along with the function signature for function
    summarization. Therefore it should be short and concise, separated
    from the rest of the 'long description' by a blank line.
    """
    import A_GIS.Code.Docstring.check_short_description
    import A_GIS.Ai.Chatbot.init

    # Only do these checks if we are not forcing AI.
    errors = A_GIS.Code.Docstring.check_short_description(
        short_description=docstring.short_description
    )
    do_ai = True if force_ai else len(errors) > 0
    if not do_ai:
        return docstring

    # Turn the errors into a directive.
    problems = ""
    if errors:
        problems = "The existing short description has these problems you should fix:\n"
        problems += "\n    -".join(errors)

    # Turn the reference code into a directive.
    reference = ""
    if docstring.reference_code:
        reference = "For reference, the code for the docstring is:\n{docstring.reference_code}"

    # Create the system prompt.
    system = f"""
You are an expert Python programmer specializing in writing short,
concise function descriptions. Your description should be no more
than 64 characters. Shorter is better.
    """

    # Create user prompt.
    user = f"""
Write a new short description for this docstring:
{docstring}

{reference}

Note, the existing short description is:
{docstring.short_description}

{problems}
"""

    # Initialize and engage the chatbot for the short description suggestion.
    # TODO: Dynamically populate these options from optimal settings.
    chatbot = A_GIS.Ai.Chatbot.init(
        model="mixtral",
        temperature=0.5,
        num_ctx=3000,
        num_predict=20,
        mirostat=2,
        system=system,
    )
    result = chatbot.chat(message=user)
    suggestion = result["message"]["content"]

    # Final fix-ups for the suggestion.
    words = suggestion.split(" ")
    words[0] = A_GIS.Text.get_word_stem(words[0]).capitalize()
    suggestion = " ".join(words)
    if len(suggestion) > 63:
        suggestion = suggestion[0:63]
    if not suggestion.endswith("."):
        suggestion = suggestion + "."

    # Final check the suggestion now meets all requirements.
    errors = A_GIS.Code.Docstring.check_short_description(
        short_description=suggestion
    )
    if len(errors) > 0:
        raise ValueError(
            f"The AI-suggested docstring short description={suggestion} fails to meet criteria with errors: {errors}."
        )

    # Update the docstring only if it meets requirements.
    docstring.short_description = suggestion

    # Return docstring.
    return docstring