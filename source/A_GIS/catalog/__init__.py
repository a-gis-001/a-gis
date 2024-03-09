def catalog(
    *,
    package_name="A_GIS",
    entry_format="{header}\n{description}",
    include_args: bool = True,
):
    import A_GIS.Code.list
    import A_GIS.Code.Docstring.get
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
            A_GIS.Code.Docstring.get(code=code, only_description=True)
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
