def function(func):
    """Decorator to enable logging
    
    This decorator logs the signature of the input arguments and output result of
    the decorated function. It also hashes the signature using `A_GIS.Text.hash`
    for unique identification. The logger is initialized with `A_GIS.Log.init()`.

    Args:
        func (callable): The function to be logged.

    Returns:
        callable: A wrapper function that logs the input and output of the
                  decorated function.

    Raises:
        None
    """

    import functools

    # Define the logging wrapper for the decorator.
    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        import logging
        import A_GIS.Text.hash
        import json
        import A_GIS.Log.init

        # Initialize the logger.
        A_GIS.Log.init()

        # Log the signature on input.
        signature = json.dumps(
            {
                "module": f"{func.__module__}",
                "function": f"{func.__name__}",
                "args": f"{args}",
                "kwargs": f"{kwargs}",
            }
        )
        s_hash = A_GIS.Text.hash(text=signature)
        logging.info(f"BEGIN_A_GIS({s_hash}) {signature}")

        # Call the function.
        result = func(*args, **kwargs)

        # Log the output for returning result.
        returned = json.dumps({"result": f"{result}"})
        logging.info(f"END_A_GIS({s_hash}) {returned}")
        return result

    return __wrapper
