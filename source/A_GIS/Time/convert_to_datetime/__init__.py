def convert_to_datetime(*, time=None):
    """Parse an ISO8601 date into a datetime object.

    This function handles ISO8601 strings with or without fractional seconds
    and with timezone information, including UTC ("Z") or offsets (e.g., "-0500").

    Args:
        time (str):
            A string representing an ISO8601 formatted date and time.

    Returns:
        datetime.datetime:
            A `datetime.datetime` object corresponding to the parsed ISO8601 string.

    Raises:
        ValueError:
            If the input string is not a valid ISO8601 format.
    """
    import datetime
    import pytz

    if not time:
        return datetime.datetime.now(pytz.utc)

    if isinstance(time, datetime.datetime):
        # If already a datetime object, ensure it has timezone information
        if time.tzinfo is None:
            return time.replace(tzinfo=pytz.utc)
        return time

    try:
        # Handle ISO8601 with timezone offset (e.g., "-0500")
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        # Handle ISO8601 with "Z" (UTC)
        try:
            return datetime.datetime.strptime(
                time, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            # Handle ISO8601 without fractional seconds and with "Z" (UTC)
            try:
                return datetime.datetime.strptime(
                    time, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=datetime.timezone.utc)
            except ValueError as e:
                raise ValueError(f"Invalid ISO8601 string: {time}") from e
