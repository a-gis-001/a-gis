def function(func):
    import functools
    import A_GIS.Log.init

    A_GIS.Log.init()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import logging
        import A_GIS.Text.hash
        import json

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

        result = func(*args, **kwargs)
        returned = json.dumps({"result": f"{result}"})
        logging.info(f"END_A_GIS({s_hash}) {returned}")

        return result

    return wrapper
