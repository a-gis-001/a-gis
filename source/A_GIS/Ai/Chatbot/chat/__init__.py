def chat(
    *,
    chatbot: type["A_GIS.Ai.Chatbot._Chatbot"],
    message: str,
    **kwargs,
):
    """Function to return a chatbot response to a message

    Use A_GIS.Ai.Chatbot.init() to create a chatbot

    """
    import A_GIS.Code.get_schema

    # Add the system message.
    if (
        len(chatbot.messages) == 0
        and chatbot.system != ""
        or (not chatbot.keep_state)
    ):
        chatbot.messages = [{"role": "system", "content": chatbot.system}]

    # Create the new messages list.
    chatbot.messages.append({"role": "user", "content": message})

    # Expand the tools.
    if len(chatbot.tools) == 0:
        for tool_name in chatbot.tool_names:
            chatbot.tools.append(A_GIS.Code.get_schema(func_path=tool_name))

    # Return the response of the chat.
    return chatbot._send_chat(
        model=chatbot.model,
        messages=chatbot.messages,
        tools=chatbot.tools,
        **chatbot.get_kwargs(**kwargs),
    )
