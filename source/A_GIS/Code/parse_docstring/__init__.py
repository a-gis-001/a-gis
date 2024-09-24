import A_GIS.Log.track_function

@A_GIS.Log.track_function
def parse_docstring(
    *,
    code: str,
    clean: bool = True,
    only_description: bool = False,
    __tracking_hash=None,
) -> str:
    """Extract and optionally cleans the first docstring.

    Extracts the first docstring from Python code, cleaning it for
    readability and providing only the main description if specified. This
    function is designed to parse the provided Python code to find and
    extract the first docstring associated with a module-level entity
    (function, class, or module). It optionally cleans up the docstring
    content for readability based on the `clean` flag and allows for
    extraction of only the main description if specified by the
    `only_description` flag. The function is instrumented with logging via
    the `A_GIS.Log.track_function` decorator to track its usage.

    Args:
        code (str):
            The Python code string from which to extract the docstring.
        clean (bool, optional):
            If True, the extracted docstring will be cleaned up for readability.
            Default is True.
        only_description (bool, optional):
            If True, returns only the main description of the docstring without
            additional sections like usage examples or parameter descriptions.
            Default is False.
        __tracking_hash (str, optional):
            An internal argument used for function tracking and logging purposes. It
            can be set to a specific hash value if needed.

    Returns:
        str:
            A string containing the cleaned docstring content if `clean` is True or
            `only_description` is False; otherwise, returns None or an
            uncleaned docstring if both flags are set to False.
    """

    import ast

    # Parse the code into an abstract syntax tree (AST)
    tree = ast.parse(code)

    # Get the docstring of the first module-level entity
    docstring = ast.get_docstring(tree)
    if not docstring:
        for x in tree.body:
            try:
                docstring = ast.get_docstring(x, clean=clean)
                break
            except BaseException:
                pass

    if docstring is not None and only_description:
        docstring = docstring.lstrip().split("\n")[0]

    return docstring
