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
        package_name (str, optional): The name of the package from which
            to list functions. Defaults to "A_GIS".

        entry_format (str, optional): A format string defining how each
            function is presented. Defaults to "{header}\\n{description}".

        include_args (bool, optional): Whether to include the function's
            signature in the header. Defaults to True.

    Returns:
        list of str: A list of formatted function entries.

    """

    import A_GIS.Code.list
    import A_GIS.Code.parse_docstring
    import A_GIS.Code.Unit.get
    import A_GIS.Code.is_function
    import A_GIS.File.read
    import pathlib
    import A_GIS.Text.add_indent

    lines = []
    result = A_GIS.Code.list(package_name=package_name)

    # Only process functions, not modules
    for name in result.functions:
        file = result.sources[name]
        code = A_GIS.File.read(file=pathlib.Path(file))
        unit = A_GIS.Code.Unit.get(code=code)
        description = (
            A_GIS.Code.parse_docstring(code=code, only_description=True)
            or "None"
        ).lstrip()

        if unit.function_definition != [""]:
            # Get just the signature part (everything after 'def
            # function_name')
            signature = "\n".join(unit.function_definition).strip()
            # Get the function name from the full path
            func_name = name.split(".")[-1]

            # Find where the actual signature starts (after the function name)
            sig_start = signature.find(func_name) + len(func_name)
            if sig_start > 0:
                # Get just the signature part
                signature = signature[sig_start:]

            if not include_args:
                header = name
            else:
                header = f"{name}{signature}"
        else:
            header = name

        text = entry_format.format(
            header=header, description=description, name=name, file=file
        )
        lines.append(text)

    return lines
