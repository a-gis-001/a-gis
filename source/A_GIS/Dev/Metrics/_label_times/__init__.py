def _label_times(labelevents):
    """Get the timeline of label changes.

    Args:
        labelevents: GitLab label events list.

    Returns:
        list: List of label event dictionaries.
    """
    import A_GIS.Time.convert_to_string

    ts = []
    for event in labelevents:
        ts.append(
            {
                "action": event.action,
                "label": event.label["name"] if event.label else None,
                "created_at": A_GIS.Time.convert_to_string(
                    time=event.created_at
                ),
            }
        )
    return ts
