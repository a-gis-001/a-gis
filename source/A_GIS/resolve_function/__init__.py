def resolve_function(*, func_path: str):
    """Resolve a function name within A_GIS."""
    import importlib

    # Split the full function name by '.'
    parts = func_path.split(".")
    module_name = ".".join(parts[:-1])
    func_name = parts[-1]

    # Import the module
    module = importlib.import_module(module_name)

    # Get the function from the module
    return getattr(module, func_name)
