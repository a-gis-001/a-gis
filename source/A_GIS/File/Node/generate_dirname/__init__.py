import A_GIS.Log.track_function

@A_GIS.Log.track_function
def generate_dirname(
    *, message: str, prefix: str = "", suffix="", __tracking_hash=None
):
    """Create a directory name from user input.

    This function initializes an AI chatbot with specific system
    instructions to generate a directory name that adheres to certain
    conventions (30 characters or less, no numbers or dates, separated
    by '-', all in lowercase). It then uses the chatbot to generate a
    response based on the provided message, slugifies the response to
    create a valid file path, and appends an optional prefix and suffix
    to the slugified name.

    Args:
        message (str):
            The input text used by the chatbot to generate the directory
            name.
        prefix (str, optional):
            An optional prefix to be added to the generated directory
            name.
        suffix (str, optional):
            An optional suffix to be appended to the generated directory
            name.

    Returns:
        dataclass:
            With the following attributes

            - dirname (str): A slugified and optionally
              prefixed/suffixed string representing the file directory
              name.
            - chat (A_GIS.Ai.Chatbot.Chat): The chatbot object that
              contains the conversation context, including the
              generated response.

    Raises:
        ValueError:
            If the generated dirname exceeds 255 characters due to the
            combination of prefix and suffix.
    """
    import A_GIS.Text.slugify
    import A_GIS.Ai.Chatbot.init
    import json

    chatbot = A_GIS.Ai.Chatbot.init(
        system="""
    You are an AI that generates simple directory names for files.
    If you are given the parent directory, your subdirectory name should
    should not repeat data from this path.
    1. 30 characters or less.
    2. No years or dates.
    3. Use '-' to separate words.
    4. Use all lower case.
    You will first brainstorm possible names. Then you will choose the best name.
    """,
        model="mistral-nemo:latest",
        num_predict=100,
        temperature=0.8,
    )

    chat = chatbot.chat(
        message=message
        + """\nReply with a JSON formatted list with 5 possible directory
    names, e.g. ["name1","name2","name3","name4","name5"].""",
        format="json",
    )
    try_list = (
        chat.response["message"]["content"]
        .replace("```json", "")
        .replace("```", "")
    )

    # Try 3 times to convert to JSON.
    for i in range(3):
        try:
            possible_dirnames = json.loads(try_list)
            break
        except BaseException as e:
            possible_dirnames = []
            pass
        chat = chatbot.chat(
            message=f"This list '{try_list}' was supposed to be in JSON format. Please try again to emit JSON with the same data.",
            format="json",
        )
        try_list = (
            chat.response["message"]["content"]
            .replace("```json", "")
            .replace("```", "")
        )

    try:
        chat = chatbot.chat(
            message="Choose the most specific descriptive directory name from this list: ["
            + (", ".join(possible_dirnames))
            + "]. Reply with a single name!"
        )
        dirname = chat.response["message"]["content"]
        dirname = A_GIS.Text.slugify(name=dirname)
        dirname = dirname.replace("_+", "-")
        if len(dirname) > 255:
            raise ValueError(
                f"Directory name {dirname} is too long (>255 characters)."
            )
    except BaseException:
        possible_dirnames = []
        dirname = "misc"
    dirname = prefix + dirname + suffix

    return A_GIS.Code.make_struct(
        dirname=dirname,
        messages=chatbot.messages,
        possible_dirnames=possible_dirnames,
    )
