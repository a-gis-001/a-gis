def move(
    *,
    old: str,
    new: str,
):
    """Move a unit within the A_GIS project structure.

    This function moves a specified unit from its current location to a
    new location, updating all references to the unit in the process. It
    ensures that the unit's codebase reflects its new name and location
    across the entire project hierarchy.

    Args:
        old (str):
            The original name of the unit (file or package) to be moved.
        new (str):
            The new name for the unit after it has been moved. This
            should follow the naming conventions expected within the
            A_GIS project.

    Returns:
        tuple[pathlib.Path, pathlib.Path]:
            A tuple containing the original path of the unit before it
            was moved and the new path where the unit has been
            successfully moved to.

    Raises:
        ValueError:
            If the new path already exists, if the new name does not
            conform to the expected naming conventions, or if there are
            any issues with the file paths or package structures during
            the move operation.
    """
    import pathlib
    import shutil
    import A_GIS.Code.find_root
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.Code.Unit.Name.check
    import A_GIS.Code.Tree.update_path_to_package
    import A_GIS.File.find_and_replace

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

    # Check the input.
    unit_type = A_GIS.Code.guess_type(file=old_file)
    check = A_GIS.Code.Unit.Name.check(name=new, unit_type=unit_type)
    if not check.result:
        raise ValueError(
            f"For A_GIS.Code.Unit.move(old={old},new={new}) the {new} name should be a proper {unit_type} name (fixed_name={check.fixed_name})."
        )

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
