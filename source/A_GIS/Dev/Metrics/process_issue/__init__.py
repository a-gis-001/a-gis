def process_issue(
    issue, store_path, *, download_images=False, attachment_url=None
):
    """Process a single GitLab issue.

    Args:
        issue (gitlab.v4.objects.Issue): GitLab issue object.
        store_path (pathlib.Path): Path to data store.
        download_images (bool, optional): Whether to download images. Defaults to False.
        attachment_url (str, optional): Base GitLab URL for image processing. Defaults to None.

    Returns:
        dict: Processed issue data.
    """
    import A_GIS.Time.convert_to_string
    import A_GIS.Dev.Metrics._get_started_at
    import A_GIS.Dev.Metrics._label_times
    import A_GIS.Dev.Metrics._extract_scl
    import A_GIS.Dev.Metrics._extract_sdl
    import A_GIS.Dev.Metrics.process_images

    labelevents = issue.resourcelabelevents.list(get_all=True)

    images, errors = A_GIS.Dev.Metrics.process_images(
        issue=issue,
        attachment_url=attachment_url,
        store_path=store_path,
        download=download_images,
    )
    for error in errors:
        if error:
            print(error)

    return {
        "title": issue.title,
        "iid": issue.iid,
        "url": issue.web_url,
        "created_at": A_GIS.Time.convert_to_string(time=issue.created_at),
        "closed_at": A_GIS.Time.convert_to_string(time=issue.closed_at),
        "started_at": A_GIS.Dev.Metrics._get_started_at(issue),
        "labels": issue.labels,
        "milestone": issue.milestone["title"] if issue.milestone else None,
        "events": A_GIS.Dev.Metrics._label_times(labelevents),
        "scl": A_GIS.Dev.Metrics._extract_scl(issue.description),
        "sdl": A_GIS.Dev.Metrics._extract_sdl(issue.description),
        "updated_at": A_GIS.Time.convert_to_string(time=issue.updated_at),
        "description": issue.description,
        "images": images,
        "weight": issue.weight or 0,
    }
