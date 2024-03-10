def init(
    *,
    filename="app.log",
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
):
    """Initializes a logger object with the given filename and log format.

	This function initializes a logging object using the specified file name and
	log message format. It returns an instance of the Log class from A_GIS.Log._Log module.

	Args:
		filename (str, optional): The name of the file where logs should be written. Defaults to "app.log".
		format (str, optional): The format string for log messages. Defaults to "%(asctime)s %(name)s - %(levelname)s - %(message)s".

	Raises:
		None

	Returns:
		Log: An instance of the Log class representing the created logger object.
    """

    import A_GIS.Log._Log

    return A_GIS.Log._Log(filename, format)
