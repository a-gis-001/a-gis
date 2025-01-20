def pack_into_function(*, code: str, function: str = None):
    """Pack all code into the last top-level unit.

    Makes a compact, self-contained unit.
    """
    import A_GIS.Code.split
    import A_GIS.Code.insert_into_function
    import A_GIS.Code.is_function
    import A_GIS.Code.collect_imports
    import A_GIS.Code.make_struct

    # Initialize returns.
    new_code = None
    imports = None
    is_function = []
    error = ""

    # Get the split code.
    split_code = A_GIS.Code.split(code=code)
    bodies = split_code.bodies
    names = split_code.names

    # Identify the function to pack into.
    function_index = -1
    if function:
        for i, name in enumerate(names):
            isf = A_GIS.Code.is_function(code=bodies[i])
            is_function.append(isf)
            if function == name:
                if isf:
                    function_index = i
                else:
                    error = f"Supplied name of {function} is not a function in code body."
                    break

        if function_index == -1 and not error:
            error = (
                f"Supplied name of {function} was not found in names {names}"
            )
    else:
        for i, body in enumerate(bodies):
            isf = A_GIS.Code.is_function(code=body)
            is_function.append(isf)
            if isf:
                function_index = i
                function = names[i]
        if function_index == -1:
            error = f"There are no functions in the code provided: {names}"

    # If a valid function index is found, process the code.
    function_code = None
    if function_index >= 0:
        function_code = bodies.pop(function_index)
        names.pop(function_index)
        imports = A_GIS.Code.collect_imports(code=code)

        # Build the addition code (imports + remaining bodies).
        addition = "\n".join(imports) + "\n\n" + "\n\n".join(bodies)
        new_code = A_GIS.Code.insert_into_function(
            code=function_code, function=function, add=addition
        )
    else:
        # Fallback to the original code if no function is found.
        new_code = code

    # Return the updated structure.
    return A_GIS.Code.make_struct(
        code=new_code,
        bodies=bodies,
        names=names,
        function_code=function_code,
        _function=function,
        is_function=is_function,
        imports=imports,
        error=error,
    )
