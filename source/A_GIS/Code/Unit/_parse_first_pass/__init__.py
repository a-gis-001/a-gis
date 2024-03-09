def _parse_first_pass(*, code: str):
    import A_GIS.Code.Docstring.modify
    import A_GIS.Code.Docstring.get

    # Get formatted lines and docstring.
    code0 = A_GIS.Code.Docstring.modify(code=code, docstring=None)
    docstring = A_GIS.Code.Docstring.get(code=code)
    lines = [line.rstrip() for line in code0.split("\n")]

    # Create type_imports, function_definition, and code_body strings.
    start_fun = False
    end_fun = False
    code_body = ""
    function_definition = ""
    type_imports = ""
    for line in lines:
        if start_fun and end_fun:
            code_body += line + "\n"
        if line.startswith("def"):
            start_fun = True
        if not start_fun:
            type_imports += line + "\n"
        if start_fun and not end_fun:
            function_definition += line + "\n"
        if start_fun and line.endswith(":"):
            end_fun = True
    function_definition = function_definition.rstrip()
    if function_definition.endswith(":"):
        function_definition = function_definition[:-1]

    return type_imports, function_definition, docstring, code_body
