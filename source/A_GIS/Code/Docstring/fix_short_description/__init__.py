def fix_short_description(
    *,
    docstring: type["A_GIS.Code.Docstring._Docstring"],
    model: str = "reflection",
    max_iterations: int = 6,
) -> str:
    """Edit docstring short descriptions for conformity.

    This function iteratively interacts with an AI chatbot to refine the
    'short description' field within a given docstring until it meets
    specified criteria or reaches the maximum number of attempts. The
    function takes into account the current state of the short
    description, identifies any issues, and uses the chatbot to generate
    a new suggestion that is concise, accurate, and properly formatted.

    Args:
        docstring (A_GIS.Code.Docstring._Docstring):
            An object representing the docstring to be edited. It must
            have attributes for `short_description`, `reference_code`,
            and potentially other information used during the refinement
            process.
        model (str, optional):
            The AI model to use for generating the short description
            suggestion. Defaults to "reflection".
        max_iterations (int, optional):
            The maximum number of iterations the function will attempt
            to improve the short description before returning the
            current best version. Defaults to 6.

    Returns:
        A_GIS.Code.Docstring._Docstring:
            An updated instance of `_Docstring` with a potentially
            improved `short_description` field based on the AI's
            suggestions and the specified criteria.
    """

    import A_GIS.Code.Docstring.check_short_description
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Ai.Chatbot.get_info
    import A_GIS.Text.get_between_tags
    import A_GIS.Text.get_root_word
    import A_GIS.Text.split_first_sentence

    # Turn the reference code into a directive.
    reference_code = ""
    if docstring.reference_code:
        reference_code = docstring.reference_code

    # Initialize and engage the chatbot for the short description suggestion.
    chatbot = A_GIS.Ai.Chatbot.init(
        model=model,
        temperature=0.7,
        num_ctx=5000,
        num_predict=30,
        mirostat=2,
        system="""
You are an AI summarization bot that creates beautiful, concise purpose statements.
Your task is to fix a Python docstring "short description", which is the first sentence
of the description which is short (~50 characters) and appears as an annotation in
many documentation resources. You will be given the current short description, the
problems, and the entire docstring and function for reference. You can think and reflect
but your new sentence should be the only thing between <output> </output> tags.
""",
    )

    for iteration in range(1, max_iterations + 1):
        # Turn the errors into a directive.
        errors = A_GIS.Code.Docstring.check_short_description(
            short_description=docstring.short_description
        )
        if len(errors) == 0:
            return docstring

        problems = "\n".join(["    - " + x for x in errors])

        # Create user prompt.
        user = f"""
The current short description:
{docstring.short_description}

Has these problems:
{problems}

The reference code is:
{reference_code}

The full docstring is:
{docstring}

This is your {iteration}/{max_iterations} attempt.

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

    return docstring
