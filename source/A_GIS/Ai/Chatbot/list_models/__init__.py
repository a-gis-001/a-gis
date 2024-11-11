def list_models(*, only_with_tools: bool = False):
    """Return a list of installed OLLaMA model names.

    This function interfaces with the OLLaMA library to obtain a list of
    all available model names. It imports the OLLaMA module, retrieves
    the list of models from the OLLaMA's `list` method, and then
    extracts the model names from this list.

    Returns:
        :
            list of str: A list containing the names of all installed
            OLLaMA models.
    """
    import ollama
    import A_GIS.Ai.Chatbot.get_info

    all_models = [entry["model"] for entry in ollama.list()["models"]]
    models = []
    for model in all_models:
        if only_with_tools:
            if not A_GIS.Ai.Chatbot.get_info(model=model).has_tools:
                continue
        models.append(model)

    return models
