def get_closure_stats(
    *, data, start_date, end_date, label="Enhancement", projections_after=None
):
    """
    Calculate closure statistics for issues within a time range, iterating through issue closure dates.

    Parameters:
        data: dict - Issue data with `started_at` and `closed_at`.
        start_date: datetime - Starting date for the calculation.
        end_date: datetime - Ending date for the calculation.

    Returns:
        list - List of tuples with date, days since start, and counts.
    """
    import A_GIS.Dev.Metrics._project_time_to_close

    def is_opened_at(issue, date):
        """Check if an issue is open on the given date."""
        return issue["started_at"] <= date <= issue["closed_at"]

    def count_is_opened_at(issues, date):
        """Count the number of issues open on the given date."""
        return sum(1 for issue in issues if is_opened_at(issue, date))

    def get_opened_at(all_issues, date):
        """Retrieve issues open on a specific date."""
        return [issue for issue in all_issues if is_opened_at(issue, date)]

    def get_closure_dates(issues):
        closure_dates = []
        for issue in issues:
            closure_dates.append(issue["closed_at"])
        return sorted(set(closure_dates))

    if not projections_after:
        projections_after = A_GIS.Dev.Metrics.get_dates(data=data,label=label)[-1]

    all_issues = []
    for v in data.values():
        if v["started_at"] and label in v["labels"]:
            x = A_GIS.Dev.Metrics._project_time_to_close(
                closed_at=v["closed_at"], started_at=v["started_at"], projections_after = projections_after
            )
            all_issues.append(
                {
                    "started_at": x.dt_started,
                    "closed_at": x.dt_closed,
                }
            )

    # Gather statistics
    stats = []
    for date1 in get_closure_dates(all_issues):
        days = []
        counts = []
        if start_date <= date1 <= end_date:
            opened_issues = get_opened_at(all_issues, date1)
            for date2 in get_closure_dates(opened_issues):
                days.append((date2 - date1).days)
                counts.append(count_is_opened_at(opened_issues, date2))
            if days:
                stats.append((date1, days, counts))

    return stats
