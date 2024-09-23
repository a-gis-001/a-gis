def catalog(
    *,
    package_name="A_GIS",
    entry_format="{header}\n{description}",
    include_args: bool = True,
):
    """Generate a catalog of functions in a package.

    This function generates a list of entries representing the functions
    available within the specified package. Each entry is formatted
    according to the `entry_format` template, which includes the
    function's header (name), its description, and the file path where
    it is defined. The description is parsed from the function's
    docstring.

    The output list of strings can be used to display or write a catalog
    in a readable format. By default, the full signature of the function
    is included in the header; this can be toggled with the
    `include_args` flag.

    Args:
        package_name (str, optional):
            The name of the package from which to list functions.
            Defaults to "A_GIS".
        entry_format (str, optional):
            A string format template that defines how each function's
            information is presented in the catalog. Defaults to
            "{header}\n{description}".
        include_args (bool, optional):
            If True, the full signature of the function will be included
            in the header. If False, only the function name without
            arguments will be used. Defaults to True.

    Returns:
        list[str]:
            A list of strings, where each string represents a formatted
            entry for a function in the package. Each entry includes the
            function's header, its description, and the file path,
            formatted according to `entry_format`.
    """

    import A_GIS.Code.list
    import A_GIS.Code.parse_docstring
    import A_GIS.Code.Unit.get
    import A_GIS.Code.is_function
    import A_GIS.File.read
    import pathlib
    import A_GIS.Text.add_indent

    lines = []
    for name, file in A_GIS.Code.list(
        package_name=package_name
    ).result.items():
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
