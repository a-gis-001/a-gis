def chat(
    *,
    chatbot: type["A_GIS.Ai.Chatbot._Chatbot"],
    message: str,
    keep_state: bool = False,
    **kwargs,
):
    """Function to return a chatbot response to a message

    Use A_GIS.Ai.Chatbot.init() to create a chatbot

    """

    # Add the system message.
    if len(chatbot.messages) == 0 and chatbot.system != "":
        messages = [{"role": "system", "content": chatbot.system}]
    else:
        messages = []

    # Create the new messages list.
    messages += chatbot.messages
    messages.append({"role": "user", "content": message})

    # Return the response of the chat.
    return chatbot._send_chat(
        model=chatbot.model,
        messages=messages,
        keep_state=keep_state,
        **chatbot.get_kwargs(**kwargs),
    )
