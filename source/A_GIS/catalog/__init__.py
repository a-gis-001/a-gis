def catalog(
    *,
    package_name="A_GIS",
    entry_format="{header}\n{description}",
    include_args: bool = True,
):
    """Generates a catalog of all functions in the specified Python package and their descriptions.

    This function retrieves a list of all code files within a given Python package using `A_GIS.Code.list`. It then reads each file, checks if it contains a function with `A_GIS.Code.is_function`, and extracts its definition with `A_GIS.Code.Unit.get`. The function description is obtained from the docstring of the code using `A_GIS.Code.parse_docstring`.

    The catalog entries are formatted according to a provided format string (entry_format), which can include placeholders for 'header', 'description', 'name', and 'file'. If the 'include_args' flag is set, function argument details will be included in the header; otherwise, only the signature of the function without arguments will be shown.

    Args:
        package_name (str, optional): The name of the Python package to catalog. Defaults to "A_GIS".
        entry_format (str, optional): A format string for each catalog entry. It must include placeholders for 'header', 'description', 'name', and 'file'. Defaults to "{header}\n{description}".
        include_args (bool, optional): If True, function argument details will be included in the header of each catalog entry. Defaults to True.

    Raises:
        None

    Returns:
        list: A list of strings, where each string is a formatted catalog entry representing a function and its description.
    """

    import A_GIS.Code.list
    import A_GIS.Code.parse_docstring
    import A_GIS.Code.Unit.get
    import A_GIS.Code.is_function
    import A_GIS.File.read
    import pathlib
    import A_GIS.Text.add_indent

    lines = []
    for name, file in A_GIS.Code.list(package_name=package_name).items():
        code = A_GIS.File.read(file=pathlib.Path(file))
        if not A_GIS.Code.is_function(code=code):
            continue
        unit = A_GIS.Code.Unit.get(code=code)
        description = (
            A_GIS.Code.parse_docstring(code=code, only_description=True)
            or "None"
        ).lstrip()
        if unit.function_definition != [""]:
            parts = name.split(".")
            signature = "\n".join(unit.function_definition).strip()
            if not include_args:
                signature = signature.split("(")[0]
            parts[-1] = signature.replace("def ", "")
            header = (".".join(parts)).lstrip()
        else:
            header = name
        text = entry_format.format(
            header=header, description=description, name=name, file=file
        )
        lines.append(text)

    return lines
