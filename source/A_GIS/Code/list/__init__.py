def list(*, package_name="A_GIS", filters=["_", "tests"]):
    """Lists all modules and sub-packages within a specified package, excluding those that start with certain filter strings.

    This function returns a dictionary where each key is the full name of a module or sub-package within the specified package,
    and each value is the file path to that module or sub-package. The modules and sub-packages are filtered out if their names
    start with any of the provided filter strings.

    Args:
        package_name (str, optional): The name of the package to search within. Defaults to "A_GIS".
        filters (list[str], optional): A list of strings that module and sub-package names should not start with.
                                       Defaults to ["_", "tests"].
    Raises:
        None

    Returns:
        dict: A dictionary mapping full module/sub-package names to their file paths within the specified package, excluding any
              modules or sub-packages that start with any of the filter strings.
    """

    import importlib
    import pathlib
    import os
    import sys
    import pkgutil

    root_package = importlib.import_module(package_name)
    package_path = root_package.__path__
    package_name = root_package.__name__

    # Iterate through all the modules and sub-packages within the package
    packages = {}
    for importer, full_name, ispkg in pkgutil.walk_packages(
        path=package_path, prefix=package_name + ".", onerror=lambda x: None
    ):
        path = importer.find_module(full_name).get_filename()

        include = True
        for x in full_name.split("."):
            for filter in filters:
                if x.startswith(filter):
                    include = False
        if include:
            packages[full_name] = path

    return packages
