def function(func):
    """Decorator to enable logging
    
    Use this to enable an AI-enabled timing capability.
    """

    import functools
    import A_GIS.Log.init

    # Define the logging wrapper for the decorator.
    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        import logging
        import A_GIS.Text.hash
        import json

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
