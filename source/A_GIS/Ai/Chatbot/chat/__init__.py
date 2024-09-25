def chat(
    *,
    chatbot: type["A_GIS.Ai.Chatbot._Chatbot"],
    message: str,
    images=[],
    **kwargs,
):
    """Send a message to start conversation with specified chatbot.

    This function allows users to engage in a chat session with an AI
    chatbot by sending a message and receiving a response. The chatbot's
    class must be an instance of `A_GIS.Ai.Chatbot._Chatbot`, which is
    expected to have a method called `chat` that takes a message and
    optional keyword arguments (`**kwargs`) and returns a response. The
    response is encapsulated within a dataclass containing the following
    attributes:

    Chatbots are created with `A_GIS.Ai.Chatbot.init` and support either
    functional `A_GIS.Ai.Chatbot.chat(chatbot=chatbot,message=message)`
    calls or object-oriented `chatbot.chat(message=message)` calls.

    Args:
        chatbot (A_GIS.Ai.Chatbot._Chatbot):
            An instance of the AI chatbot class that will handle the
            conversation.
        message (str):
            The text message to send to the chatbot.
        **kwargs:
            Additional keyword arguments that may be used by the chatbot
            to process the message.

    Returns:
        dataclass:
            A named tuple with the following attributes:

            - messages (list of str): All messages exchanged during
              the conversation.
            - response (str): The final response from the chatbot.
            - tool_response (Optional[str]): Additional response if
              the chatbot is also a tool, or `None`.
    """

    # Return the response of the chat. Note that the chatbot's messages sent
    # as an argument are modified.
    # _send_chat implementation must return a dataclass with
    #   - messages: list of messages at exit
    #   - response: response to chat
    #   - tool_response: response to tool request (or None if no tools)
    return chatbot.chat(message=message, images=images, **kwargs)
