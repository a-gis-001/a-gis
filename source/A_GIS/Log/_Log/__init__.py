class _Log:
    initialized = False
    current_filename = None
    current_format = None

    def __init__(self, filename, format):
        reinitialize = False
        if filename is not None or _Log.current_filename != filename:
            _Log.current_filename = filename
            reinitialize = True
        if format is not None or _Log.current_format != format:
            _Log.current_format = format
            reinitialize = True
        if reinitialize or not initialized:
            self._do_initialize()

    @staticmethod
    def _do_initialize():
        import logging

        # Remove all handlers associated with the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Reconfigure logging with the new settings
        logging.basicConfig(
            level=logging.INFO,
            filename=_Log.current_filename,
            filemode="w",
            format=_Log.current_format,
        )

        # Inform about the initialization
        logging.info(
            f"Logger initialized to use file: {_Log.current_filename} with format: {_Log.current_format}"
        )

        _Log.initialized = True
