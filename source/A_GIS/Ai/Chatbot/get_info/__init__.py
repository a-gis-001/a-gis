def get_info(*, model: str):
    """Get AI model info from the name."""
    import ollama
    import re
    import A_GIS.Code.make_struct
    import A_GIS.Ai.Chatbot.list_models

    context_length = None
    has_tools = None
    available_models = A_GIS.Ai.Chatbot.list_models()
    available = model in available_models

    if available:
        try:
            data = ollama.show(model=model)
            pattern = r"context_length['\"]\s*:\s*(\d+),"
            match = re.search(
                pattern, str(data["model_info"]).replace("\n", " ")
            )
            if match:
                context_length = int(match.group(1))
            has_tools = data["template"].find(".Tools") >= 0

        except BaseException:
            pass

    return A_GIS.Code.make_struct(
        model=model,
        available=available,
        context_length=context_length,
        has_tools=has_tools,
        available_models=available_models,
    )
