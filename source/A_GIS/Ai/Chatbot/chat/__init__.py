def chat(
    *,
    chatbot: type["A_GIS.Ai.Chatbot._Chatbot"],
    message: str,
    images=[],
    **kwargs,
):
    """Start a conversation with an AI chatbot.

    This function facilitates communication with an instance of the
    `Chatbot` class, allowing the user to send both text and image
    content for processing. The chatbot responds with text, potentially
    interacts with tools if applicable, and returns a structured
    response containing all relevant information.

    Args:
        chatbot (A_GIS.Ai.Chatbot._Chatbot):
            An instance of the AI chatbot that will handle the
            conversation.
        message (str):
            The text message to be sent to the chatbot for processing
            and response.
        images (list(str), optional):
            A list of image file paths or URLs to be sent alongside the
            message. If an empty list, no images are sent.
        **kwargs (dict, optional):
            Additional keyword arguments that may be accepted by the
            chatbot for processing.

    Returns:
        dataclass:
            A structured response object with the following attributes:

            - messages (list(str)): A list of all messages exchanged
              between the user and the chatbot during this session,
              including any images sent.
            - response (str): The text response from the chatbot based
              on the message and images provided.
            - tool_response (str|None, optional): The response from
              any tools invoked by the chatbot as part of processing
              the message or images. This will be `None` if no tools
              were used.
    """
    import copy

    # Return the response of the chat. Note that the chatbot's messages sent
    # as an argument are modified.
    # _send_chat implementation must return a dataclass with
    #   - messages: list of messages at exit
    #   - response: response to chat
    #   - tool_response: response to tool request (or None if no tools)
    chatbot2 = copy.deepcopy(chatbot)
    response = chatbot2.chat(message=message, images=images, **kwargs)
    response.chatbot = chatbot2
    return response
