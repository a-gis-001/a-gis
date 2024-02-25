def get(*, code: str, clean: bool = True) -> str | None:
    """
    Extracts the docstring from a string of Python code.

    This function parses the provided Python code into an abstract syntax tree (AST),
    and then retrieves the docstring of the first module-level entity (usually a
    function, class, or the module itself).

    Parameters:
    code: A string representing the Python code.

    Returns:
    The docstring found in the code, if any; otherwise, returns None.
    """
    import ast

    # Parse the code into an abstract syntax tree (AST)
    tree = ast.parse(code)

    # Get the docstring of the first module-level entity
    for x in tree.body:
        try:
            return ast.get_docstring(x, clean=clean)
        except:
            pass

    return None
