def list_models():
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

    return [entry["model"] for entry in ollama.list()["models"]]
