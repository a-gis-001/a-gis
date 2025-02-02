def filter_issues(*, data, label=None, closed_only=False):
    """Filter issues by label and closed status.

    Args:
        data (dict): Dictionary of issue data.
        label (str, optional): Label to filter by. Defaults to None.
        closed_only (bool, optional): Whether to filter only closed issues. Defaults to False.

    Returns:
        dict: Filtered data.
    """
    import A_GIS.Dev.Metrics._filter_by_label
    import A_GIS.Dev.Metrics._filter_closed_only

    filtered_data = A_GIS.Dev.Metrics._filter_by_label(
        data, label
    )
    filtered_data = A_GIS.Dev.Metrics._filter_closed_only(
        filtered_data, closed_only
    )
    return filtered_data
