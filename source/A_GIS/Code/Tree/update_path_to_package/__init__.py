def update_path_to_package(
    *, path: type["pathlib.Path"], root: type["pathlib.Path"] = None
):
    """Create all parent package paths

    uses A_GIS Unit standards

    """

    import A_GIS.File.touch
    import A_GIS.File.write
    import A_GIS.File.read
    import A_GIS.Code.find_root

    if root is None:
        root = A_GIS.Code.find_root(path=path, throw_if_not_found=True)

    child = path
    while child != root:
        parent = child.parent
        package_file = parent / "__init__.py"
        A_GIS.File.touch(path=package_file)
        code = A_GIS.File.read(file=package_file)

        # Use A_GIS standards to tell if a function.
        if child.name[0].islower():
            import_statement = "from ." + child.name + " import " + child.name
        else:
            import_statement = "from . import " + child.name

        if code.find(import_statement) < 0:
            code += (
                "\n\n#Temporary add from A_GIS.Code.Tree.update_path_to_package\n"
                + import_statement
            )
            A_GIS.File.write(content=code, file=package_file)
        child = parent
