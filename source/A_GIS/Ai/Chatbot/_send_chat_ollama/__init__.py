import A_GIS.Log.track_function

@A_GIS.Log.track_function
def _send_chat_ollama(
    *,
    model: str,
    messages: list[dict],
    tools=[],
    __tracking_hash=None,
    **kwargs,
):
    """Send chatbot chat request through ollama."""
    import ollama
    import json
    import A_GIS.resolve_function
    import A_GIS.Code.make_struct
    import A_GIS.Ai.Chatbot.get_info
    import copy

    # First round chat. If tools would be used, then will go to second round.
    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        options=ollama.Options(**kwargs),
    )
    messages.append(response["message"])

    # Handle tool interaction.
    tool_response = None
    if A_GIS.Ai.Chatbot.get_info(model=model).has_tools:
        if tool_calls := messages[-1].get("tool_calls", None):
            for tool_call in tool_calls:
                if fn_call := tool_call.get("function"):
                    # Put together tool call.
                    fn_name: str = fn_call["name"]
                    fn_args: dict = fn_call["arguments"]

                    # We only support A_GIS functions which return something
                    # which converts to a dict.
                    fn_res: str = json.dumps(
                        A_GIS.resolve_function(func_path=fn_name)(
                            **fn_args
                        ).__dict__
                    )

                    # Add the tool call result to the messages.
                    messages.append(
                        {
                            "role": "tool",
                            "name": fn_name,
                            "content": fn_res,
                        }
                    )

            # The previous response becomes the tool response.
            tool_response = copy.deepcopy(response)

            # Second round chat, now with the results of the tools.
            response = ollama.chat(
                model=model,
                messages=messages,
                tools=tools,
                options=ollama.Options(**kwargs),
            )
            messages.append(response["message"])

    # Return a results struct.
    return A_GIS.Code.make_struct(
        messages=messages, response=response, tool_response=tool_response
    )
