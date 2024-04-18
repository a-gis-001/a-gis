def fix_short_description(
    *,
    docstring: type["A_GIS.Code.Docstring._Docstring"],
    force_ai=False,
    model: str = "mixtral",
) -> str:
    """Improve function's short description using AI, if needed.

    This function fixes the short description of a function's docstring
    using AI-generated suggestions. It checks the existing short
    description for any issues and suggests corrections through an AI
    model. The AI model is only engaged when issues are identified or
    when `force_ai` is set to True.

    Args:
        docstring (A_GIS.Code.Docstring._Docstring):
            The docstring object of the function.
        force_ai (bool, optional):
            If True, AI assistance will be used regardless of whether issues are
            present in the short description.

    Returns:
        str:
            The updated docstring with a new or improved short description.

    Raises:
        ValueError:
            If the AI-suggested short description does not meet all requirements.
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
        problems += "\n".join(["    - " + x for x in errors])

    # Turn the reference code into a directive.
    reference = ""
    if docstring.reference_code:
        reference = f"For reference, the code for the docstring is:\n{docstring.reference_code}"

    # Create the system prompt.
    system = f"""
You are an expert Python programmer specializing in writing short,
concise function descriptions. Your description should be no more
than 63 characters. The first word of the description should be a
simple verb stem, e.g. 'Run' not 'Runs' or 'Ran'. The short
description should be a full sentence and end with a period.
Avoid abbreviations and punctuation.
    """

    # Create user prompt.
    user = f"""
Write a new short description for this docstring:
{docstring}

{reference}

Note, the existing short description is:
{docstring.short_description}

{problems}

IMPORTANT: REPLY WITH ONLY THE 63 CHARACTER SHORT DESCRIPTION ON A SINGLE LINE!
ANYTHING AFTER 63 CHARACTERS WILL BE REMOVED. 63 CHARACTERS IS 9 WORDS OR LESS.
"""

    # Initialize and engage the chatbot for the short description suggestion.
    # TODO: Dynamically populate these options from optimal settings.
    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        temperature=0.7,
        num_ctx=3000,
        num_predict=100,
        mirostat=2,
        system=system,
    )
    result = chatbot.chat(message=user)

    # Strip layers of junk.
    suggestion = result["message"]["content"].strip().strip("'\"").strip()

    # Keep first line.
    suggestion = suggestion.split("\n")[0]

    # Only keep the first sentence.
    suggestion, _ = A_GIS.Text.split_first_sentence(text=suggestion)

    # Force first word to be stem.
    words = suggestion.split(" ")
    words[0] = A_GIS.Text.get_root_word(word=words[0]).capitalize()
    suggestion = " ".join(words)

    # Force last char to be period.
    if not suggestion.endswith("."):
        suggestion = suggestion + "."

    # Final check the suggestion now meets all requirements.
    errors = A_GIS.Code.Docstring.check_short_description(
        short_description=suggestion
    )
    if len(errors) > 0:
        raise ValueError(
            f"The AI-suggested docstring short description='{suggestion}' fails to meet criteria with errors: {errors}."
        )

    # Update the docstring only if it meets requirements.
    docstring.short_description = suggestion

    # Return docstring.
    return docstring
