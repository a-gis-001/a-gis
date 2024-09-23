def init(
    *,
    provider: type["A_GIS.Ai.Chatbot._Provider.types_allowed"] = "ollama",
    model: str = "deepseek-coder:33b",
    system: str = "You are a helpful assistant.",
    mirostat=2,
    num_predict=5000,
    num_ctx=10000,
    temperature=0.5,
    messages=[],
    tool_names=[],
    keep_state: bool = False,
) -> type["A_GIS.Ai.Chatbot._Chatbot"]:
    """
    Initializes and returns a chatbot model based on the specified provider.

    Redirects to init_from_<provider> where <provider>.

    Args:
        model (str): The model name or identifier to be initialized.
        provider (ProviderLiteral): The provider from which to initialize the model. Defaults to 'ollama'.

    Returns:
        A_GIS.Ai.Chatbot._Chatbot: An instance of the chatbot model initialized from the specified provider.

    """
    import A_GIS.Ai.Chatbot._Chatbot

    # Check name is allowed.
    names_allowed = A_GIS.Ai.Chatbot._Provider.names_allowed
    if provider not in names_allowed:
        raise ValueError(
            f"Provider={provider} not recognized! Should be one of: {names_allowed}"
        )

    # Dynamic import based on provider
    module = f"A_GIS.Ai.Chatbot._send_chat_{provider}"
    function = f"_send_chat_{provider}"
    imported_module = __import__(module, fromlist=[function])
    _send_chat = getattr(imported_module, function)
    return A_GIS.Ai.Chatbot._Chatbot(
        provider=provider,
        model=model,
        system=system,
        mirostat=mirostat,
        num_predict=num_predict,
        num_ctx=num_ctx,
        temperature=temperature,
        _send_chat=_send_chat,
        messages=messages,
        tool_names=tool_names,
        tools=[],
        keep_state=keep_state,
    )
