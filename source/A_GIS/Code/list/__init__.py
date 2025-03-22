def list(
    *,
    package_name="A_GIS",
    ignore=["_", "tests"],
    functions_only: bool = False,
):
    """List all modules and functions in a package.

    Args:
        package_name: Name of package to list contents of
        ignore: List of strings to ignore in module names
        functions_only: Whether to only return functions

    Returns:
        A_GIS.Code.make_struct containing:
            modules: List of module names
            functions: List of function names
            sources: Dict mapping names to their source files
            _package_name: Original package name
            _ignore: Ignored patterns
    """
    import A_GIS.Code.make_struct
    import importlib
    import pkgutil
    import inspect
    import sys
    import typing

    # Get package path
    package = importlib.import_module(package_name)
    package_path = package.__path__

    modules = []
    functions = []
    sources = {}  # Maps names to their source files

    # Walk through all modules
    for importer, full_name, ispkg in pkgutil.walk_packages(
        path=package_path, prefix=package_name + ".", onerror=lambda x: None
    ):
        # Get module path using find_spec instead of find_module
        spec = importer.find_spec(full_name)
        if spec is None or spec.origin is None:
            continue

        path = spec.origin

        include = True
        for x in full_name.split("."):
            if any(x.startswith(i) for i in ignore):
                include = False
                break

        if not include:
            continue

        if not functions_only:
            modules.append(full_name)
            sources[full_name] = path

        try:
            module = importlib.import_module(full_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and obj.__module__ == full_name:
                    full_func_name = f"{full_name}.{name}"
                    functions.append(full_func_name)
                    sources[full_func_name] = path
        except Exception as e:
            print(f"Error importing {full_name}: {e}", file=sys.stderr)
            continue

    return A_GIS.Code.make_struct(
        modules=sorted(modules),
        functions=sorted(functions),
        sources=sources,
        _package_name=package_name,
        _ignore=ignore,
    )
