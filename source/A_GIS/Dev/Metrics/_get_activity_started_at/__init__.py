def _get_activity_started_at(labelevents):
    """Get the earliest activity start time from label events.

    Args:
        labelevents: GitLab label events list.

    Returns:
        datetime: The earliest activity start time, or None if no activity.
    """
    import A_GIS.Time.convert_to_datetime

    activity_started_at = None
    relevant_labels = {
        "1-selected",
        "2-in-progress",
        "3-in-review",
        "4-in-staging",
    }

    for event in labelevents:
        if (
            event.action == "add"
            and event.label
            and event.label["name"] in relevant_labels
        ):
            event_time = A_GIS.Time.convert_to_datetime(time=event.created_at)
            if activity_started_at is None or event_time < activity_started_at:
                activity_started_at = event_time

    return activity_started_at
