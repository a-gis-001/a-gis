def _get_completed(*, data, only_actual=False, label="Enhancement"):
    """Get completed issues with a particular label."""
    import A_GIS.Dev.Metrics._project_time_to_close

    issues = []
    last_closed_date = None
    for v in data.values():
        if only_actual and not v["closed_at"]:
            continue
        if v["started_at"] and label in v["labels"]:
            x = A_GIS.Dev.Metrics._project_time_to_close(
                closed_at=v["closed_at"], started_at=v["started_at"]
            )
            if x.dt_closed:
                if not last_closed_date:
                    last_closed_date = x.dt_closed
                if x.dt_closed > last_closed_date:
                    last_closed_date = x.dt_closed
            issues.append(
                {
                    "days": x.days_to_close,
                    "closed_at": x.dt_projected_closed,
                    "started_at": x.dt_started,
                    "_value": v,
                }
            )
    return issues, last_closed_date
