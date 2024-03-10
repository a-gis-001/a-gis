def guess_type(
    *, file: type["pathlib.Path"] = None, code: str = "", filename: str = ""
):
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
