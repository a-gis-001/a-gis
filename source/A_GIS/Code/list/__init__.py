def list(
    *,
    package_name="A_GIS",
    ignore=["_", "tests"],
    functions_only: bool = False,
):
    """Retrieve package modules and sub-packages with filtering.

    This function retrieves all modules and sub-packages from a given
    Python package, as specified by `package_name`. It filters out any
    modules or sub-packages that match the patterns in the `ignore`
    list. Additionally, if `functions_only` is True, it will only
    include items identified as functions using `A_GIS.Code.guess_type`.
    The resulting data structure contains the full names and paths of
    the included modules and packages.

    Args:
        package_name (str, optional):
            The name of the package to list. Defaults to "A_GIS".
        ignore (list, optional):
            A list of patterns to exclude from the listing. Defaults to
            ["_", "tests"].
        functions_only (bool, optional):
            If True, only include items that are identified as
            functions. Defaults to False.

    Returns:
        dataclass:
            With the following attributes

            - result (dict): A dictionary mapping full module names to
              their paths.
            - package_name (str): The name of the package from which
              modules and sub-packages were listed.
            - ignore (list): A list of patterns that were used to
              exclude certain items.
            - ignored (list): A list of full module names that were
              excluded based on the `ignore` patterns.
    """

    import importlib
    import pathlib
    import os
    import sys
    import pkgutil
    import A_GIS.Code.make_struct
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.Code.guess_type

    root_package = importlib.import_module(package_name)
    package_path = root_package.__path__
    package_name = root_package.__name__

    # Iterate through all the modules and sub-packages within the package
    ignored = []
    packages = {}
    for importer, full_name, ispkg in pkgutil.walk_packages(
        path=package_path, prefix=package_name + ".", onerror=lambda x: None
    ):
        path = importer.find_module(full_name).get_filename()

        include = True
        for x in full_name.split("."):
            for filter in ignore:
                if x.startswith(filter):
                    ignored.append(full_name)
                    include = False
        if (
            functions_only
            and A_GIS.Code.guess_type(file=pathlib.Path(path)) != "function"
        ):
            include = False
        if include:
            packages[full_name] = str(path)

    return A_GIS.Code.make_struct(
        result=packages,
        package_name=package_name,
        ignore=ignore,
        ignored=ignored,
    )
