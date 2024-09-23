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
    import ollama
    import json
    import A_GIS.resolve_function
    import A_GIS.Code.make_struct
    import A_GIS.Ai.Chatbot.get_info

    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        options=ollama.Options(**kwargs),
    )

    messages.append(response["message"])

    if A_GIS.Ai.Chatbot.get_info(model=model).has_tools:
        tool_response = None
        if tool_calls := messages[-1].get("tool_calls", None):
            for tool_call in tool_calls:
                if fn_call := tool_call.get("function"):
                    fn_name: str = fn_call["name"]
                    fn_args: dict = fn_call["arguments"]

                    fn_res: str = json.dumps(
                        A_GIS.resolve_function(func_path=fn_name)(
                            **fn_args
                        ).__dict__
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "name": fn_name,
                            "content": fn_res,
                        }
                    )

            tool_response = response
            response = ollama.chat(
                model=model,
                messages=messages,
                tools=tools,
                options=ollama.Options(**kwargs),
            )
            messages.append(response["message"])

    return A_GIS.Code.make_struct(
        messages=messages, response=response, tool_response=response
    )
