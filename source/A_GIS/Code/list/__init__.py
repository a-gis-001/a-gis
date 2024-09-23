def list(*, package_name="A_GIS", ignore=["_", "tests"]):
    """List sub-packages within a specified package, excluding those with matching prefixes.

    This function retrieves and lists all sub-packages within a
    specified package that are not excluded by the provided ignore. It
    returns a structured representation of the package's contents,
    including the paths to the modules or packages that were included
    based on the ignore.

    Args:
        package_name (str, optional):
            The name of the package to list sub-packages from. Defaults
            to "A_GIS".
        ignore (list of str, optional):
            A list of strings representing prefixes to include or
            exclude when filtering modules and sub-packages. By default,
            includes "_" and "tests".

    Returns:
        dataclass:
            With the following attributes

            - result (dict): A dictionary where keys are full names of
              included packages/modules and values are their
              corresponding file paths as strings.
            - package_name (str): The name of the package from which
              the sub-packages were listed.
            - ignore (list of str): The list of ignore used to
              determine inclusion or exclusion of modules and sub-
              packages.
            - ignored (list of str): A list of full names of
              packages/modules that were included based on the
              ignore.
    """

    import importlib
    import pathlib
    import os
    import sys
    import pkgutil
    import A_GIS.Code.make_struct

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
        if include:
            packages[full_name] = str(path)

    return A_GIS.Code.make_struct(
        result=packages,
        package_name=package_name,
        ignore=ignore,
        ignored=ignored,
    )
