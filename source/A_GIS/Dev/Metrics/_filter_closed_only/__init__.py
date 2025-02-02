def _filter_closed_only(data, closed_only):
    """Filter data dictionary to only include closed issues.

    Args:
        data (dict): Dictionary of issue data.
        closed_only (bool): Whether to filter for only closed issues.

    Returns:
        dict: Filtered data containing only closed issues if closed_only is True.
    """
    if not closed_only:
        return data
    return {k: v for k, v in data.items() if v.get("closed_at") is not None}
