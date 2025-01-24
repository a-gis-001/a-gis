def get_dates(*, data, key="closed_at", label=None, unique=False):
    """
    Extract and return a sorted list of dates from the issue data based on the specified key.

    Args:
        data (dict): The issue data containing `started_at` and `closed_at` dates.
        key (str): The key to extract dates from each issue (default is 'closed_at').

    Returns:
        list: A sorted list of dates.
    """
    import A_GIS.Time.convert_to_datetime
    
    dates = []
    for issue in data.values():
        if key in issue and issue[key]:
            if not label or (label in issue["labels"]):
                dates.append(A_GIS.Time.convert_to_datetime(time=issue[key]))
    if unique:
        dates = set(dates)
    return sorted(dates)
