def list_models():
    """List locally available models."""
    import ollama

    return [entry["model"] for entry in ollama.list()["models"]]
