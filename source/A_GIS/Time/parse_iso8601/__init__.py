import datetime

def parse_iso8601(*, time: str | datetime.datetime):
    """Parse an ISO8601 date and time string or return a datetime object as-is.

    This function takes a single parameter, `time`, which can either
    be a string formatted according to the ISO8601 standard for date and time
    representations, or a `datetime.datetime` object. If the input is a
    `datetime.datetime`, it is returned directly without modification. If the
    input is a string, it is parsed into a `datetime.datetime` object.

    Args:
        time (str | datetime.datetime):
            An ISO8601 formatted string or a `datetime.datetime` object.

    Returns:
        datetime.datetime:
            A `datetime.datetime` object corresponding to the parsed
            ISO8601 string or the original input if it is already a
            `datetime.datetime`. If `time` is `None` or empty, returns `None`.

    Raises:
        ValueError:
            If the input string is not a valid ISO8601 format.
    """
    if not time:
        return None

    if isinstance(time, datetime.datetime):
        # If already a datetime object, return it as-is
        return time

    try:
        # Attempt to parse ISO8601 format with timezone 'Z'
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # Handle cases with missing fractional seconds
        try:
            return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as e:
            raise ValueError(f"Invalid ISO8601 string: {time}") from e
