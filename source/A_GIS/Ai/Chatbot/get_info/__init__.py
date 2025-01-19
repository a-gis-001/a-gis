def get_info(*, model: str):
    """Retrieve information about a specified AI chatbot model.

    This function interacts with the OLLama API to fetch detailed
    information about the capabilities and settings of the given chatbot
    model. It returns a structured object containing various attributes
    related to the model's availability, configuration, and whether it
    includes tool integration features.

    Args:
        model (str):
            The identifier for the AI chatbot model you want to retrieve
            information about.

    Returns:
        A_GIS.Code.make_struct.Struct:
            An instance of a dataclass with the following attributes:

            - model (str): The model identifier for which the
              information was retrieved.
            - available (bool): Indicates whether the specified model
              is available in the list of models.
            - context_length (int | None): The maximum token length
              that the model can handle, if available. Otherwise,
              None.
            - has_tools (bool | None): Indicates whether the model
              includes tool integration capabilities. Otherwise, None.
            - available_models (list | str of str): A list or a string
              representing all available chatbot models.
            - output_tag (str | None): An optional tag associated with
              the model's output, if available. Otherwise, None.
    """
    import ollama
    import re
    import A_GIS.Code.make_struct
    import A_GIS.Ai.Chatbot.list_models

    context_length = None
    has_tools = None
    available_models = A_GIS.Ai.Chatbot.list_models()
    available = model in available_models
    output_tag = None

    if available:
        try:
            data = ollama.show(model=model)
            pattern = r"context_length['\"]\s*:\s*(\d+),"
            match = re.search(pattern, str(data).replace("\n", " "))
            if match:
                context_length = int(match.group(1))
            has_tools = str(data).index(".Tools") >= 0

        except BaseException:
            pass

    return A_GIS.Code.make_struct(
        model=model,
        available=available,
        context_length=context_length,
        has_tools=has_tools,
        available_models=available_models,
        output_tag=output_tag,
    )
