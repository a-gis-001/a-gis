def list(*, package_name="A_GIS", filters=["_", "tests"]):
    """List modules and sub-packages in a Python package dynamically.

    This function dynamically lists all the modules and sub-packages
    contained within the specified Python package, optionally filtered
    by a list of prefixes. It returns a dictionary where each key is the
    full name of a module or sub-package within the package, and each
    value is the corresponding file path on the filesystem.

    Args:
        package_name (str, optional):
            The name of the package to list modules from. Defaults to
            "A_GIS".
        filters (list(str), optional):
            A list of prefixes to filter the modules and sub-packages
            by. If a module or sub-package name starts with any of the
            provided prefixes, it will be excluded from the results.
            Defaults to ["_", "tests"].

    Returns:
        dict:
            A dictionary where each key is a full name (relative to the
            package) of a module or sub-package within the specified
            package, and each value is the corresponding file path (as a
            `pathlib.Path` object) on the filesystem.
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
