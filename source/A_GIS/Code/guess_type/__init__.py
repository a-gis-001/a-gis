def guess_type(
    *, file: type["pathlib.Path"] = None, code: str = "", filename: str = ""
):
    """Determine the type of a given file based on its content.

    This function attempts to determine the type of a file by analyzing
    its content and filename. It can identify whether the file is a
    package, class, function, or program. If no file is provided, it
    will prompt the user for input from the console. The type of the
    file is returned as a string.

    Args:
        file (pathlib.Path, optional):
            A pathlib.Path object representing the file to be analyzed.
            If None, the function will attempt to open and read from the
            user's input from the console.
        code (str, optional):
            The content of the file as a string. Defaults to an empty
            string. This parameter is primarily for internal use when a
            file object is not provided.
        filename (str, optional):
            The name of the file to be analyzed. Defaults to an empty
            string. This parameter is primarily for internal use when a
            file object is not provided.

    Returns:
        str:
            A string indicating the type of the file content. It can be
            one of the following:

            - "package" if the file appears to be a Python package.
            - "class" if the file contains a class definition.
            - "function" if the file contains a function definition.
            - "program" if the file is a script or executable code
              with a filename.
            - "unknown" if the file does not match any of the above
              criteria.
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
