class _Log:
    initialized = False
    logfile = None
    name = None

    def __init__(self):
        if not _Log.initialized:
            self._do_initialize()

    @staticmethod
    def _do_initialize():
        import logging
        import structlog
        import os

        if _Log.initialized:
            return

        _Log.name = "A_GIS_LOG"
        _Log.logfile = os.environ.get("A_GIS_LOGFILE", "app.log")

        shared_processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        # Configure basic logging
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(_Log.logfile, mode="a"),
            ],
        )

        final_processors = [
            structlog.processors.JSONRenderer(indent=1, sort_keys=True)
        ]

        structlog.configure(
            processors=shared_processors + final_processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        _Log.logger = structlog.get_logger(_Log.name)
        _Log.logger.info(f"{_Log.name} initialized")
        _Log.initialized = True
