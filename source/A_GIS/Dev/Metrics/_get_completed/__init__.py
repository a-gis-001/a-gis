def _get_completed(*, data, only_actual=False, label="Enhancement"):
    """Get completed issues with a particular label."""

    issues = []
    last_closed_date = None
    for v in data.values():
        if only_actual and not v["closed_at"]:
            continue
        if v["started_at"] and label in v["labels"]:
            days, closed_date, started_date, projected_closed = calculate_days(
                v["closed_at"], v["started_at"]
            )
            if closed_date:
                if not last_closed_date:
                    last_closed_date = closed_date
                if closed_date > last_closed_date:
                    last_closed_date = closed_date
            issues.append(
                {
                    "days": days,
                    "closed_at": projected_closed,
                    "started_at": started_date,
                    "_value": v,
                }
            )
    return issues, last_closed_date
