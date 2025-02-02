def _filter_by_label(data, label):
    """Filter data dictionary by label.

    Args:
        data (dict): Dictionary of issue data.
        label (str): Label to filter by.

    Returns:
        dict: Filtered data containing only issues with the specified label.
    """
    if not label:
        return data
    return {k: v for k, v in data.items() if label in v.get("labels", [])}
