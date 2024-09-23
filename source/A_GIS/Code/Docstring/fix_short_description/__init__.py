def fix_short_description(
    *,
    docstring: type["A_GIS.Code.Docstring._Docstring"],
    model: str = "reflection",
    max_iterations: int = 10,
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

    Returns:
        str:
            The updated docstring with a new or improved short description.
    """

    import A_GIS.Code.Docstring.check_short_description
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Ai.Chatbot.get_info
    import A_GIS.Text.get_between_tags
    import A_GIS.Text.get_root_word
    import A_GIS.Text.split_first_sentence

    # Turn the reference code into a directive.
    reference = ""
    if docstring.reference_code:
        reference = f"For reference, the code we are documenting is:\n{docstring.reference_code}"

    # Initialize and engage the chatbot for the short description suggestion.
    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        temperature=0.7,
        num_ctx=5000,
        num_predict=30,
        mirostat=2,
    )

    for iteration in range(1, max_iterations + 1):
        # Turn the errors into a directive.
        errors = A_GIS.Code.Docstring.check_short_description(
            short_description=docstring.short_description
        )
        if len(errors) == 0:
            return docstring

        problems = ""
        problems = (
            "Attempt {iteration}/{max_iterations}. Fix these problems :\n"
        )
        problems += "\n".join(["    - " + x for x in errors])

        # Create user prompt.
        user = f"""
Replace the current short description:
{docstring.short_description}

of the python docstring:
{docstring}

{reference}

{problems}

Do not forget to provide your final response inside <output> tags.
        """

        response = chatbot.chat(message=user, keep_state=True).response

        # Get the new suggestion.
        suggestion = A_GIS.Text.get_between_tags(
            text=response["message"]["content"],
            begin_tag="<output>",
            end_tag="</output>",
        )
        if not suggestion:
            suggestion = docstring.short_description

        # Strip extra characters.
        suggestion = suggestion.strip().strip("'\"").strip()

        # Keep first line only.
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

        # Update the docstring only if it meets requirements.
        docstring.short_description = suggestion

    # Return docstring.
    return docstring
