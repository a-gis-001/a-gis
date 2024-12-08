import A_GIS.Log.track_function

@A_GIS.Log.track_function
def _send_chat_openai(
    *, model: str, messages: list[dict], __tracking_hash=None, **kwargs
):
    import openai
    import os

    api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)

    available_models = ["gpt-4o", "gpt-4o-mini"]
    openai_model = ""
    for available_model in available_models:
        if available_model.startswith(model):
            openai_model = available_model
    if openai_model == "":
        raise ValueError(
            f"Provided model={model} does not match any available models: {available_models}!"
        )

    max_tokens = kwargs["num_ctx"] + kwargs["num_predict"]
    if max_tokens > 4096:
        max_tokens = 4096
    completion = client.chat.completions.create(
        messages=messages,
        model=openai_model,
        temperature=kwargs["temperature"],
        max_tokens=max_tokens,
    )
    result = completion.__dict__
    result["message"] = {"content": completion.choices[0].message.content}

    return result
