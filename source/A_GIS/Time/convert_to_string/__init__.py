def convert_to_string(
    *, time, timezone="US/Eastern", format="%Y-%m-%dT%H:%M:%S.%fZ"
):
    """Convert a datetime object or ISO8601 string to an ISO8601 formatted string.

    This function takes an optional parameter `time`, which can be
    an instance of `datetime.datetime` or an ISO8601-formatted string.

    Args:
        time (datetime.datetime or str):
            The `datetime.datetime` object or ISO8601 string to be formatted.

        timezone (str, optional):
            The name of the timezone to convert the datetime to. Defaults to 'US/Eastern'.

    Returns:
        str:
            A string representing the input `datetime.datetime` object or string
            in ISO8601 format, including the local time zone offset.
    """
    import datetime
    import pytz

    if time is None:
        return None

    if isinstance(time, str):
        try:
            # Parse the string into a datetime object (assuming UTC by default)
            time = datetime.datetime.strptime(time, format).replace(
                tzinfo=pytz.utc
            )
        except ValueError as e:
            raise ValueError(f"Invalid ISO8601 string: {time}") from e

    if isinstance(time, datetime.datetime):
        # Convert to the specified timezone
        local_time = time.astimezone(pytz.timezone(timezone))
        # Return ISO8601 format with timezone offset
        return local_time.strftime(format)

    raise TypeError("time must be a datetime.datetime or an ISO8601 string.")
