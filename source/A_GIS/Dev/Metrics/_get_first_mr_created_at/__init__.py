def _get_first_mr_created_at(issue):
    """Get the creation time of the first merge request.

    Args:
        issue: GitLab issue object.

    Returns:
        datetime: Creation time of the first merge request, or None if no MRs.
    """
    import A_GIS.Time.convert_to_datetime
    
    first_mr_created_at = None

    for mr in issue.related_merge_requests(get_all=True):
        mr_created_at = A_GIS.Time.convert_to_datetime(time=mr["created_at"])
        if first_mr_created_at is None or mr_created_at < first_mr_created_at:
            first_mr_created_at = mr_created_at
            
    return first_mr_created_at
