import A_GIS.Log.track_function

@A_GIS.Log.track_function
def _send_chat_ollama(
    *, model: str, messages: list[dict], __tracking_hash=None, **kwargs
):
    import ollama

    return ollama.chat(
        model=model, messages=messages, options=ollama.Options(**kwargs)
    )
