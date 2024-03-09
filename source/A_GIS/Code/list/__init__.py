def list(*, package_name="A_GIS", filters=["_", "tests"]):
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
