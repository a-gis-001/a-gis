import A_GIS.Log.track_function

@A_GIS.Log.track_function
def _send_chat_groq(
    *, model: str, messages: list[dict], __tracking_hash=None, **kwargs
):
    import groq
    import os

    api_key = os.environ.get("GROQ_API_KEY")
    client = groq.Groq(api_key=api_key)

    available_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]
    groq_model = ""
    for available_model in available_models:
        if available_model.startswith(model):
            groq_model = available_model
    if groq_model == "":
        raise ValueError(
            f"Provided model={model} does not match any available models: {available_models}!"
        )

    completion = client.chat.completions.create(
        messages=messages,
        model=groq_model,
        temperature=kwargs["temperature"],
        max_tokens=kwargs["num_ctx"] + kwargs["num_predict"],
    )
    result = completion.__dict__
    result["message"] = {"content": completion.choices[0].message.content}

    return result
