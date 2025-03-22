def get_schema(*, func_path: str):
    """Generate a function's schema from its docstring and type hints.

    This function analyzes a given function's documentation and type
    hints to create a structured schema object. The schema includes the
    function's name, description, and parameter information with types
    and descriptions. It is useful for understanding how to call the
    function and what parameters it expects.

    Args:
        func_path (str): The path or identifier of the function for which the schema
            should be generated.

    Returns:
        dict: A dictionary representing the schema of the function. The
            schema includes:

            - "type": A string indicating that the schema represents a
              function
            - "function": An object containing:
                - "name": The name of the function as specified by
                  `func_path`
                - "description": A combined description of the
                  function, formatted with a short and long
                  description from the function's docstring
                - "parameters": An object representing the
                  parameters of the function.
    """
    import inspect
    import typing
    import A_GIS.Code.Docstring.init
    import A_GIS.resolve_function

    # Get the function name
    func = A_GIS.resolve_function(func_path=func_path)

    # Get the function description (docstring)
    docstring = A_GIS.Code.Docstring.init(text=func.__doc__)
    description = (
        docstring.short_description
        + "\n\n"
        + (docstring.long_description or "")
    )
    params_dict = {}
    for param in docstring.params:
        if param.arg_name.startswith("_"):
            continue
        params_dict[param.arg_name] = {
            "type": param.type_name,
            "description": param.description,
        }

    # Get the function signature and type hints
    signature = inspect.signature(func)
    type_hints = typing.get_type_hints(func)

    # Parameters for the schema
    parameters = {}
    required_params = []

    for param_name, param in signature.parameters.items():
        if param_name.startswith("_"):
            continue

        # Define parameter schema
        param_schema = {
            "type": "string"  # Default to string if no type hint is provided
        }

        # If the parameter has a type hint, add it to the schema
        if param_name in type_hints:
            hint_type = type_hints[param_name]
            if hint_type == str:
                param_schema["type"] = "string"
            elif hint_type == int:
                param_schema["type"] = "integer"
            elif hint_type == float:
                param_schema["type"] = "number"
            elif hint_type == bool:
                param_schema["type"] = "boolean"
            elif hint_type == list:
                param_schema["type"] = "array"
            else:
                param_schema["type"] = params_dict[param_name]["type"]

        # Add description for the parameter if available in the docstring.
        param_schema["description"] = params_dict[param_name]["description"]

        # Add to required if no default value is present
        if param.default == inspect.Parameter.empty:
            required_params.append(param_name)

        # Add parameter schema to the parameters list
        parameters[param_name] = param_schema

    # Build the final schema
    return {
        "type": "function",
        "function": {
            "name": func_path,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required_params,
            },
        },
    }
