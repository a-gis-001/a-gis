def list(
    *,
    package_name="A_GIS",
    ignore=["_", "tests"],
    functions_only: bool = False,
):
    """Retrieve modules and sub-packages within a package.

    The `list` function takes three optional parameters that allow you
    to specify the package to list, a list of names to ignore during the
    listing process, and a flag to consider only functions within the
    package. It returns a structured representation of the found modules
    and sub-packages.

    Args:
        package_name (str, optional):
            The name of the package to be listed. Defaults to "A_GIS".
        ignore (list of str, optional):
            A list of names to be ignored during the listing process.
            Defaults to ["_", "tests"].
        functions_only (bool, optional):
            If True, only functions within the package will be listed.
            Defaults to False.

    Returns:
        dataclass:
            With the following attributes

            - result (dict): A dictionary with module or sub-package
              names as keys and their corresponding file paths as
              values.
            - package_name (str): The name of the root package whose
              contents are being listed.
            - ignore (list of str): A list of names that were ignored
              during the listing process.
            - ignored (list of str): A list of names that were found
              but were ignored due to the `ignore` parameter.

    Raises:
        ValueError:
            If a module or sub-package cannot be found using the
            provided file path.
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
