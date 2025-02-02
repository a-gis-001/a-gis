def _get_started_at(issue):
    """Get the time when work started on an issue.

    Args:
        issue (gitlab.v4.objects.Issue): GitLab issue object.

    Returns:
        str: ISO format datetime string or None if not started.
    """
    import A_GIS.Time.convert_to_string
    import A_GIS.Dev.Metrics._extract_scl
    import A_GIS.Dev.Metrics._get_first_mr_created_at
    import A_GIS.Dev.Metrics._get_activity_started_at

    # If there is no SCL it did not start yet.
    if A_GIS.Dev.Metrics._extract_scl(issue.description) is None:
        return None

    # Retrieve the first merge request creation time
    first_mr_created_at = A_GIS.Dev.Metrics._get_first_mr_created_at(issue)

    # Get label events and retrieve the first activity time
    labelevents = issue.resourcelabelevents.list(get_all=True)
    activity_started_at = A_GIS.Dev.Metrics._get_activity_started_at(
        labelevents
    )

    # Return the earliest time
    if first_mr_created_at and activity_started_at:
        return A_GIS.Time.convert_to_string(
            time=min(first_mr_created_at, activity_started_at)
        )
    elif first_mr_created_at:
        return A_GIS.Time.convert_to_string(time=first_mr_created_at)
    elif activity_started_at:
        return A_GIS.Time.convert_to_string(time=activity_started_at)
    return None
