def distill(*, code: str) -> str:
    """Distill code to only executable code and imports

    This function parses the input Python code into an Abstract Syntax 
    Tree (AST) using the `ast` module in Python's standard library. It 
    then walks through all nodes in the AST, identifying and replacing 
    docstrings and multiline string literals with empty strings.

    Please note that due to the nature of how Python parses ASTs and 
    comments, comments (which start with '#') are not included in the 
    AST and hence are not present in the unparsed code, effectively 
    removing them from the output.

    Args:
        code (str):
            The Python code string to be distilled.

    Returns:
        str:
            The distilled Python code as a string, with docstrings and 
            multiline string literals removed.

    Examples:
        >>> ds=('"'*3) + 'I am a docstring!' + ('"'*3)
        >>> test_code = f'''
        ... def example_function(param1, param2):
        ...     {ds}
        ...     # This is a comment.
        ...     return (param1, param2)
        ... '''
        >>> print(distill(code=test_code))
        def example_function(param1, param2):
            return (param1, param2)
    """

    import ast
    import re
    import A_GIS.Code._distill_imports

    # Parse the code into an abstract syntax tree (AST).
    # Walk through all nodes in the AST to identify docstrings and multiline
    # string literals, and replace them with standard strings.
    parsed = ast.parse(code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            node.value = ast.Constant(value="")

    # Fix imports.
    distilled_code = A_GIS.Code._distill_imports(code=code)

    # Remove any blank lines or blank docstrings.
    distilled_code = re.sub(
        r'^\s*""""""\s*$\n', "", ast.unparse(parsed), flags=re.MULTILINE
    )
    distilled_code = re.sub(r"\n\s*\n", "\n", distilled_code)

    # Return final distilled code.
    return distilled_code
