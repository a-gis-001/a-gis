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
    import shutil
    import A_GIS.Code.find_root
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.Code.Unit.Name.check
    import A_GIS.Code.Tree.update_path_to_package
    import A_GIS.File.find_and_replace

    # Check the input.
    if not A_GIS.Code.Unit.Name.check(name=new):
        raise ValueError(
            f"For A_GIS.Code.Unit.move(old={old},new={new}) the {new} name be a proper functional unit name."
        )

    # Get the necessary variables.
    old_path = A_GIS.Code.Unit.Name.to_path(name=old)
    root = A_GIS.Code.find_root(path=old_path)
    old_name = old.split(".")[-1]
    new_name = new.split(".")[-1]
    old_file = old_path / "__init__.py"
    old_package = old_path.parent / "__init__.py"
    new_path = A_GIS.Code.Unit.Name.to_path(name=new, check_exists=False)
    if new_path.exists():
        raise ValueError("Cannot move {old} to existing path {new_path}")

    # Replace in original old file.
    A_GIS.File.find_and_replace(
        files=[old_file], old="def " + old_name, new="def " + new_name
    )

    # Replace in all files.
    A_GIS.File.find_and_replace(files=root.rglob("*.py"), old=old, new=new)

    # Replace in parent package file.
    A_GIS.File.find_and_replace(
        files=[old_package],
        old="from ." + old_name + " import " + old_name,
        new="",
    )

    # Move the old directory to new directory.
    shutil.move(old_path, new_path)

    # Traverse through the new package hierarchy and make sure everything
    # exists.
    A_GIS.Code.Tree.update_path_to_package(path=new_path)

    # Return the final path pair.
    return old_path, new_path
