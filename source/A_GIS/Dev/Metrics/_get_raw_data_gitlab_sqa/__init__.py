def _get_raw_data_gitlab_sqa(
    *,
    url,
    project_number,
    api_key_env="GITLAB_API_KEY",
    store="data.json",
    only_from_store=False,
    save_every=15,
    full_update=False,
    label=None,
    closed_only=False,
    download_images=False,
    issue_number=None,
):
    """Assumes specific things about how things are managed within gitlab

    Args:
        url (str): The GitLab URL.
        project_number (int): The GitLab project number.
        api_key_env (str, optional): The environment variable containing the API key. Defaults to "GITLAB_API_KEY".
        store (str, optional): The file to store data in. Defaults to "data.json".
        only_from_store (bool, optional): Whether to only read from store. Defaults to False.
        save_every (int, optional): How often to save to store. Defaults to 15.
        full_update (bool, optional): Whether to force full update. Defaults to False.
        label (str, optional): Filter issues by label. Defaults to None.
        closed_only (bool, optional): Filter to only include closed issues. Defaults to False.
        download_images (bool, optional): Whether to download image attachments. Defaults to False.
        issue_number (int, optional): Specific issue number to fetch. Defaults to None.

    Returns:
        dict: The raw data filtered by label and/or closed status if specified.
    """
    import pathlib
    import tqdm.notebook
    import os
    import A_GIS.Time.convert_to_string
    import A_GIS.Dev.Metrics.filter_issues
    import A_GIS.Dev.Metrics.process_issue
    import gitlab

    if pathlib.Path(store).exists():
        only_keys = [issue_number] if issue_number is not None else None
        data = A_GIS.Data.Format.Json.load_from_db(
            file=store, leave=False, only_keys=only_keys
        )
    else:
        data = {}

    # Quick return for store-only requests
    if only_from_store:
        filtered_data = A_GIS.Dev.Metrics.filter_issues(
            data=data, label=label, closed_only=closed_only
        )
        if issue_number:
            return {
                k: v for k, v in filtered_data.items() if k == issue_number
            }
        return filtered_data

    api_key = os.getenv(api_key_env)
    store_path = pathlib.Path(store)

    gl = gitlab.Gitlab(url, private_token=api_key)
    p = gl.projects.get(project_number)
    attachment_url = f"{gl.url}/-/project/{project_number}"

    count = 0
    cached_data = {}
    issues_list = []
    if issue_number:
        target = p.issues.get(issue_number)
        if target:
            issues_list = [target]
    else:
        issues_list = p.issues.list(iterator=True)
    skipped = 0
    updated = 0
    with tqdm.notebook.tqdm(issues_list) as pbar:
        for f in pbar:
            pbar.set_postfix(
                {"id": f.iid, "skipped": skipped, "updated": updated}
            )
            if not full_update:
                if f.iid in data:
                    if data[f.iid][
                        "updated_at"
                    ] == A_GIS.Time.convert_to_string(time=f.updated_at):
                        skipped += 1
                        continue

            # Skip if we're filtering by label and this issue doesn't have it
            if label and label not in f.labels:
                skipped += 1
                continue

            # Skip if we're only looking for closed issues and this one isn't
            # closed
            if closed_only and not f.closed_at:
                skipped += 1
                continue

            updated += 1
            data[f.iid] = A_GIS.Dev.Metrics.process_issue(
                issue=f,
                store_path=store_path,
                download_images=download_images,
                attachment_url=attachment_url,
            )
            cached_data[f.iid] = data[f.iid]
            count += 1
            if count % save_every == 0:
                A_GIS.Data.Format.Json.save_to_db(
                    data=cached_data, file=store, leave=False
                )
                count = 0
                cached_data = {}

    # Final save to get anything left over.
    A_GIS.Data.Format.Json.save_to_db(
        data=cached_data, file=store, leave=False
    )

    # Apply all filters before returning
    return A_GIS.Dev.Metrics.filter_issues(
        data=data, label=label, closed_only=closed_only
    )
