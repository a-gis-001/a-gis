def init_from_file(*, file: type["pathlib.Path"]):
    """Initializes a tree object from a given Python file.

    This function reads the content of a Python file and guesses its type (module or script),
    name and full name based on its path. It then initializes a tree object with this information
    and the code read from the file. If the provided file is a directory, it assumes an '__init__.py'
    file exists in that directory. If the file does not exist, it raises a ValueError.

    Args:
        file (pathlib.Path): The path to the Python file to be read and used to initialize
                              the tree object.

    Raises:
        ValueError: If the provided file does not exist.

    Returns:
        A_GIS.Code.Tree._Tree: An instance of the Tree class representing the code structure
                                 from the given Python file.
    """

    import A_GIS.Code.Tree._Tree
    import A_GIS.Code.Tree._Visitor
    import A_GIS.File.read
    import A_GIS.Code.Tree.init
    import A_GIS.Code.guess_type
    import A_GIS.Code.guess_name

    if file.is_dir():
        file /= "__init__.py"

    if not file.exists():
        raise ValueError(f"init_from_file: file='{file}' does not exist!")

    code = A_GIS.File.read(file=file)
    _type = A_GIS.Code.guess_type(code=code, filename=file.name)
    full_name = A_GIS.Code.guess_name(path=file)
    name = full_name.split(".")[-1]

    return A_GIS.Code.Tree.init(
        _type=_type, file=file, name=name, full_name=full_name, code=code
    )
