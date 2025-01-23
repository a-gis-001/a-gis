def get(
    *,
    year=None,
    month=1,
    day=1,
    hours=0,
    minutes=0,
    seconds=0,
    timezone="US/Eastern",
):
    """Get a datetime object"""

    import datetime
    import pytz

    if not year:
        d = datetime.datetime.now()
    else:
        d = datetime.datetime(year, month, day, hours, minutes, seconds)

    return pytz.timezone(timezone).localize(d)
