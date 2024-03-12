def init(*args, **kwargs):
    """Initializes a logging object with a specified filename and log format.

    This function initializes a Logger instance using the provided file name and log format string.
    It returns an instance of the Log class from A_GIS.Log._Log module.

    Args:
        filename (str, optional): The name of the file where logs should be written. Defaults to "app.log".
        format (str, optional): The format string for log messages. Defaults to "%(asctime)s %(name)s - %(levelname)s - %(message)s".

    Raises:
        None

    Returns:
        Log: An instance of the Log class representing the created logger object.
    """

    import A_GIS.Log._Log

    A_GIS.Log._Log().logger.info(*args, **kwargs)
