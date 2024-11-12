def get_source(*, entity, depth=0, max_depth=2):
    """Retrieve the source code of a Python module or function.

    This function attempts to import the specified `entity` as a module
    or extracts the module and function from a fully qualified entity
    name. It then retrieves the source code for either the entire module
    or the specified function, including any called functions up to a
    specified depth limit. This can be used to analyze dependencies and
    understand the structure of the code.

    Args:
        - entity (str):
            The identifier for the module or the fully qualified name of
            a function within that module.
        - depth (int, optional):
            The maximum recursion depth to trace called functions.
            Defaults to 0.
        - max_depth (int, optional):
            The maximum allowed depth for tracing called functions.
            Defaults to 2.

    Returns:
        dict:
            A dictionary with keys as the identifiers of the modules or
            functions and values as strings containing the source code
            or error messages.
        
            - If `entity` is a module, the dictionary will have keys
              as the names of classes, functions, and methods within
              that module, and their corresponding source codes.
            - If `entity` is a fully qualified function name, the
              dictionary will contain the source code for that
              function and its called functions up to the specified
              depth.

    Raises:
        - ModuleNotFoundError:
            If the module specified by `entity` cannot be found.
        - ValueError:
            If `entity` is not in a format that can be split into a
            module and a function name.
    """
    import inspect
    import ast
    import importlib
    sources = {}

    try:
        # Attempt to load the entity as a module
        module = importlib.import_module(entity)
        func_name = None
    except ModuleNotFoundError:
        try:
            # If not a module, split the entity into module and function parts
            module_name, func_name = entity.rsplit('.', 1)
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            return {entity: f"Module not found: {e}"}
        except ValueError as e:
            return {entity: f"Invalid entity format: {e}"}

    # If only a module is provided, retrieve the entire module source
    if func_name is None:
        try:
            module_source = inspect.getsource(module)
            sources[module.__name__] = module_source
        except Exception as e:
            sources[module.__name__] = f"Unable to retrieve source: {e}"
    else:
        # If a function is specified, retrieve its source
        try:
            func = getattr(module, func_name)
            sources[func_name] = inspect.getsource(func)
        except Exception as e:
            return {entity: f"Unable to retrieve source: {e}"}

    # Helper function to get called functions within source code
    def get_called_functions(func_source):
        func_ast = ast.parse(func_source)
        called_functions = []
        for node in ast.walk(func_ast):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):  # Direct function call
                    called_functions.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):  # Method or attribute access
                    # Handle cases like `obj.method` or `module.func`
                    try:
                        if hasattr(node.func.value, 'id'):
                            called_functions.append(f"{node.func.value.id}.{node.func.attr}")
                    except AttributeError:
                        pass
        return called_functions

    # Recursive function to get sources
    def retrieve_sources(func_name, module, depth):
        if depth > max_depth:
            return
        try:
            func = getattr(module, func_name)
            func_source = inspect.getsource(func)
            sources[func_name] = func_source
            for called in get_called_functions(func_source):
                try:
                    # Try to parse `module.function` format
                    if '.' in called:
                        called_module_name, called_func_name = called.rsplit('.', 1)
                        try:
                            called_module = importlib.import_module(called_module_name)
                        except ModuleNotFoundError:
                            # Module not found, skip this function
                            sources[called] = f"Module {called_module_name} not found."
                            continue
                        retrieve_sources(called_func_name, called_module, depth + 1)
                    else:
                        # Handle standalone functions if available
                        retrieve_sources(called, module, depth + 1)
                except Exception as e:
                    # Handle functions that are not accessible or can't be imported
                    sources[called] = f"Unable to retrieve source: {e}"
        except Exception as e:
            sources[func_name] = f"Unable to retrieve source: {e}"

    # Start the recursive source retrieval from the main function or entire module
    if func_name:
        retrieve_sources(func_name, module, depth)
    else:
        # If only a module is provided, retrieve all functions in the module
        for name, func in inspect.getmembers(module, inspect.isfunction):
            retrieve_sources(name, module, depth)

    return sources
