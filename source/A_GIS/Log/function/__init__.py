def function(func):
    """Decorator to enable logging

    This decorator logs the signature of the input arguments and output result of
    the decorated function. It also hashes the signature using `A_GIS.Text.hash`
    for unique identification. The logger is initialized with `A_GIS.Log.append()`.

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
        import A_GIS.Text.hash
        import json
        import A_GIS.Log.append

        # Log the signature on input.
        signature = json.dumps(
            {
                "module": f"{func.__module__}",
                "function": f"{func.__name__}",
                "args": f"{args}",
                "kwargs": f"{kwargs}",
            }
        )
        tracking_hash = A_GIS.Text.hash(text=signature)
        A_GIS.Log.append(
            tracking_hash_on_entry=tracking_hash, args=args, kwargs=kwargs
        )

        # Call the function.
        result = func(*args, **kwargs, __tracking_hash=tracking_hash)

        # Log the output for returning result.
        A_GIS.Log.append(tracking_hash_on_exit=tracking_hash, output=result)
        return result

    return __wrapper
