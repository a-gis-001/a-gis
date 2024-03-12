def move(
    *,
    old: str,
    new: str,
):
    """Move and rename an A_GIS code functional unit

    This function requires the input old and new to be valid full
    names, e.g. A_GIS.X.Y.z.

    The old one must exist.

    """
    import pathlib
    import A_GIS.File.read
    import A_GIS.File.write
    import shutil
    import A_GIS.Code.find_root
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.Code.Unit.Name.check

    # Check the input.
    if not A_GIS.Code.Unit.Name.check(name=old):
        raise ValueError(
            f"For A_GIS.Code.Unit.move(old={old},new={new}) the {old} must be a proper functional unit name."
        )
    if not A_GIS.Code.Unit.Name.check(name=new):
        raise ValueError(
            f"For A_GIS.Code.Unit.move(old={old},new={new}) the {new} name be a proper functional unit name."
        )

    # Get the old path and the root.
    old_path = A_GIS.Code.Unit.Name.to_path(name=old)
    if not old_path.exists():
        raise ValueError(f"Could not find file {old_path} for {old}!")
    root = A_GIS.Code.find_root(path=old_path)

    # Replace name in old.
    old_name = old.split(".")[-1]
    new_name = new.split(".")[-1]
    old_file = old_path / "__init__.py"
    code = A_GIS.File.read(file=old_file)
    code = code.replace("def " + old_name, "def " + new_name, 1)
    A_GIS.File.write(content=code, file=old_file)

    # Replace fully qualified names: old to new.
    for file in root.rglob("*.py"):
        code = A_GIS.File.read(file=file)
        code = code.replace(old, new)
        A_GIS.File.write(content=code, file=file)

    # Remove the old name from the old package.
    old_package = old_path.parent / "__init__.py"
    code = A_GIS.File.read(file=old_package)
    code = code.replace("from ." + old_name + " import " + old_name, "")
    A_GIS.File.write(content=code, file=old_package)

    # Get the new path.
    new_path = A_GIS.Code.Unit.Name.to_path(name=new)
    if new_path.exists():
        raise ValueError("Cannot move {old} to existing path {new_path}")

    # Traverse through the new package hierarchy and make sure everything
    # exists.
    child_path = new_path
    package_path = new_path.parent
    while package_path.parent != root:
        package_file = package_path / "__init__.py"
        A_GIS.File.touch(path=package_file)
        code = A_GIS.File.read(file=package_file)
        code += (
            "\n" + "from ." + child_path.name + " import " + child_path.name
        )
        A_GIS.File.write(content=code, file=package_file)
        child_path = child_path.parent
        package_path = package_path.parent

    # Finally move the old path.
    shutil.move(old_path, new_path)
    return old_path, new_path
