def _project_time_to_close(*, closed_at, started_at, projections_after=None):
    """Generate a projection of the time to close a project.

    This function calculates the projected time to close a project based on the
    start date and either the actual close date or the current date if the project
    is still open. If the project is not yet closed, it estimates the close time
    as twice the duration from the start date to the current date.

    Args:
        closed_at (str): The date when the project was closed, in a string format
            that can be converted to a datetime object. If None, the project is
            considered open.
        started_at (str): The date when the project started, in a string format
            that can be converted to a datetime object.
        projections_after (datetime, optional): The current date and time. If None, the current
            date is fetched and adjusted to the most recent Saturday.

    Returns:
        A structure containing:
            - days_to_close (int): The number of days from start to close.
            - dt_closed (datetime or None): The datetime object of the close date,
              or None if the project is still open.
            - dt_started (datetime): The datetime object of the start date.
            - dt_projected_closed (datetime): The projected close date.
    """
    import A_GIS.Time.get
    import A_GIS.Time.convert_to_datetime
    import A_GIS.Code.make_struct
    import datetime

    def _get_current_date():
        """Fetch and adjust the current date to the most recent Saturday."""
        current_date = A_GIS.Time.get()
        days_since_saturday = (current_date.weekday() - 5) % 7
        return current_date - datetime.timedelta(days=days_since_saturday)

    def _calculate_close_time(dt_started, dt_closed, projections_after):
        """Calculate the close time and projected close date."""
        if dt_closed and dt_closed < projections_after:
            days_to_close = (dt_closed - dt_started).days
        else:
            days_to_close = 2 * (projections_after - dt_started).days
            dt_closed = dt_started + datetime.timedelta(days=days_to_close)
        return days_to_close, dt_closed

    if started_at is None:
        return A_GIS.Code.make_struct(
            days_to_close=None, dt_closed=None, dt_started=None
        )

    projections_after = projections_after or _get_current_date()
    dt_started = A_GIS.Time.convert_to_datetime(time=started_at)

    days_to_close, dt_closed = _calculate_close_time(
        dt_started,
        A_GIS.Time.convert_to_datetime(time=closed_at),
        projections_after,
    )

    return A_GIS.Code.make_struct(
        days_to_close=days_to_close, dt_closed=dt_closed, dt_started=dt_started
    )
