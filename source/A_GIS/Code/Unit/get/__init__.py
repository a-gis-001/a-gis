def get(*, code: str):
    """Parse code into a functional unit
    
    Separates the code into four main sections 
    
    - type imports
    - function definition
    - docstring
    - code body
    
    The function also reorganizes the code body string into a list of blocks. 
    Finally, it returns an instance of the `_Unit` data class with these split parts.

    Args:
        code (str): The full code to be processed.

    Raises:
        None

    Returns:
        _Unit: An instance of the `_Unit` data class representing the split and organized code units.
    """

    import A_GIS.Code.Unit._parse_first_pass
    import A_GIS.Code.Unit._Unit

    # Split the full code body into 4 expected sections.
    type_imports0, function_definition0, docstring0, code_body0 = (
        A_GIS.Code.Unit._parse_first_pass(code=code)
    )

    # Reorganize the code body string into unit.
    code_body = []
    block = []
    for line in code_body0.split("\n"):
        if line == "":
            if len(block) > 0:
                code_body.append(block)
            block = []
        else:
            block.append(line)

    # Initialize others.
    type_imports = (
        None if len(type_imports0) == 0 else type_imports0.split("\n")
    )
    docstring = None if not docstring0 else docstring0.split("\n")
    function_definition = function_definition0.split("\n")

    # Return a _Unit data class type.
    return A_GIS.Code.Unit._Unit(
        type_imports, function_definition, docstring, code_body
    )
