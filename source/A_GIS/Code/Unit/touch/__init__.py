def touch(*, name: str):
    """Touch an A_GIS code functional unit by name or path

    Note this is intended to be used within A_GIS to easily create
    new functional units.
    """

    import pathlib
    import A_GIS.File.touch
    import A_GIS.Code.Tree.update_path_to_package

    if "." in name:
        path = (
            A_GIS.Code.Unit.Name.to_path(name=name, check_exists=False)
            / "__init__.py"
        )
    else:
        path = pathlib.Path(name).resolve()
        if not path.suffix:
            path /= "__init__.py"

    # First get the root.
    root = A_GIS.Code.find_root(path=__file__, throw_if_not_found=True)

    # Then create the new file and all the package inits on the way up.
    module = path.parent.name
    touch_path = A_GIS.File.touch(
        path=path, content_if_empty=f"def {module}():\n    pass"
    )
    A_GIS.Code.Tree.update_path_to_package(path=path.parent, root=root)

    return touch_path
