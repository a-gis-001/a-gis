def get_sublogger(*, name, file_name, backup_days=30, prune_interval=86400):
    """Get a logger for a specific sub application"""

    import logging
    import os
    import time

    class _Sublogger(logging.FileHandler):
        def __init__(
            self, file_name, backup_days, prune_interval, delay=False
        ):
            super().__init__(
                file_name, mode="a", encoding="utf-8", delay=delay
            )
            self.file_name = file_name
            self.backup_days = backup_days
            self.last_prune = 0
            self.prune_interval = prune_interval
            # Do not override self.lock

        def emit(self, record):
            self.acquire()
            try:
                super().emit(record)
                now = time.time()
                if now - self.last_prune > self.prune_interval:
                    self.last_prune = now
                    self.prune_log()
            finally:
                self.release()

        def prune_log(self):
            self.acquire()
            try:
                temp_file_name = self.baseFilename + ".tmp"
                cutoff_time = (
                    time.time() - self.backup_days * 86400
                )  # 30 days in seconds

                with (
                    open(
                        self.baseFilename, "r", encoding=self.encoding
                    ) as read_file,
                    open(
                        temp_file_name, "w", encoding=self.encoding
                    ) as write_file,
                ):

                    for line in read_file:
                        timestamp_str = line.split(" - ")[0]
                        try:
                            log_time_struct = time.strptime(
                                timestamp_str, "%Y-%m-%d %H:%M:%S"
                            )
                            log_timestamp = time.mktime(log_time_struct)
                            if log_timestamp >= cutoff_time:
                                write_file.write(line)
                        except ValueError:
                            write_file.write(line)

                os.replace(temp_file_name, self.file_name)
            except Exception:
                self.handleError(None)
            finally:
                self.release()

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create an instance of the custom handler
    handler = _Sublogger(
        file_name=file_name,
        backup_days=backup_days,
        prune_interval=prune_interval,
    )

    # Define a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
