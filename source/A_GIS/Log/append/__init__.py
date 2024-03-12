def append(*args, **kwargs):
    """Appends to the log

    Args:
        any data

    Raises:
        None

    """

    import A_GIS.Log._Log

    A_GIS.Log._Log().logger.info(*args, **kwargs)
