def move(
    *,
    root: type["pathlib.Path"],
    old: type["pathlib.Path"],
    new: type["pathlib.Path"],
):

    import pathlib
    import A_GIS.File.read
    import A_GIS.File.write
    import shutil

    if not old.is_dir():
        raise ValueError(f"{old} must be a directory")

    # Recursively find all Python files and replace.
    old2 = ".".join(old.with_suffix("").parts)
    new2 = ".".join(new.with_suffix("").parts)
    for file in root.rglob("*.py"):
        code = A_GIS.File.read(file=file)
        code = code.replace(old2, new2)
        A_GIS.File.write(content=code, file=file)

    # Replace name in parent.
    parent = old.parent / "__init__.py"
    old_name = old.with_suffix("").name
    new_name = new.with_suffix("").name
    code = A_GIS.File.read(file=parent)
    code = code.replace(old_name, new_name)
    A_GIS.File.write(content=code, file=parent)

    # Replace name in actual.
    actual = old / "__init__.py"
    code = A_GIS.File.read(file=actual)
    code = code.replace("def " + old_name, "def " + new_name)
    A_GIS.File.write(content=code, file=actual)

    shutil.move(old, new)
