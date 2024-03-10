def guess_type(
    *, file: type["pathlib.Path"] = None, code: str = "", filename: str = ""
):
    """Guesses the type of a given code snippet or file based on its content.

    This function uses other helper functions to determine the type of a given
    code snippet or file. It first checks if the code is a package, then it
    checks for a class, function, program, and finally returns 'unknown' if no
    matching type could be found.

    Args:
        file (pathlib.Path, optional): The path to the Python file to analyze. If provided, the file will be read and its content will be used instead of the 'code' argument.
        code (str, optional): A string containing the Python code to analyze. This is only used if 'file' is not provided.
        filename (str, optional): The name of the file being analyzed. This is only used in conjunction with the 'code' argument.

    Raises:
        None

    Returns:
        str: A string representing the type of the code or file. Possible return values are 'package', 'class', 'function', 'program', and 'unknown'.
    """

    import A_GIS.Code.is_class
    import A_GIS.Code.is_function
    import A_GIS.Code.is_program
    import A_GIS.Code.is_package
    import A_GIS.File.read
    import pathlib

    if file is not None:
        filename = file.name
        if code == "":
            code = A_GIS.File.read(file=file)

    # Main guessing logic
    if A_GIS.Code.is_package(code=code, filename=filename):
        return "package"
    elif A_GIS.Code.is_class(code=code):
        return "class"
    elif A_GIS.Code.is_function(code=code):
        return "function"
    elif A_GIS.Code.is_program(code=code, filename=filename):
        return "program"
    else:
        return "unknown"
