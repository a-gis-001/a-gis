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
    
    Returns:
        dict: The raw data filtered by label and/or closed status if specified.
    """
    import pathlib
    import datetime
    import tqdm.notebook
    import re
    import sys
    import os
    import A_GIS.Time.convert_to_datetime
    import A_GIS.Time.convert_to_string
    import A_GIS.Dev.Metrics._get_raw_data_gitlab_sqa
    import gitlab

    def filter_by_label(data, label):
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

    def filter_closed_only(data, closed_only):
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

    def apply_filters(data, label=None, closed_only=False):
        """Apply all filters to the data.
        
        Args:
            data (dict): Dictionary of issue data.
            label (str, optional): Label to filter by. Defaults to None.
            closed_only (bool, optional): Whether to filter for only closed issues. Defaults to False.
            
        Returns:
            dict: Filtered data based on specified criteria.
        """
        filtered_data = filter_by_label(data, label)
        filtered_data = filter_closed_only(filtered_data, closed_only)
        return filtered_data

    def get_activity_started_at(labelevents):
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
                event_time = A_GIS.Time.convert_to_datetime(
                    time=event.created_at
                )
                if (
                    activity_started_at is None
                    or event_time < activity_started_at
                ):
                    activity_started_at = event_time

        return activity_started_at

    def get_first_mr_created_at(issue):
        first_mr_created_at = None

        for mr in issue.related_merge_requests(get_all=True):
            mr_created_at = A_GIS.Time.convert_to_datetime(
                time=mr["created_at"]
            )
            if (
                first_mr_created_at is None
                or mr_created_at < first_mr_created_at
            ):
                first_mr_created_at = mr_created_at

        return first_mr_created_at

    def get_started_at(issue):
        # If there is no SCL it did not start yet.
        if extract_scl(issue.description) is None:
            return None

        # Retrieve the first merge request creation time
        if get_first_mr_created_at(issue) is None:
            return None

        # Retrieve the activity started time
        return A_GIS.Time.convert_to_string(
            time=get_activity_started_at(
                issue.resourcelabelevents.list(get_all=True)
            )
        )

    def label_times(labelevents):
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

    def extract_scl(issue_text):
        # Match the ## SQA section and look for the Change log number within it
        sqa_section = re.search(r"## SQA(.*?)(##|$)", issue_text, re.DOTALL)
        if sqa_section:
            # Extract the content of the ## SQA section
            sqa_content = sqa_section.group(1)
            # Look for the Change log number within the ## SQA section
            change_log_match = re.search(
                r"Change log number:\s*(SCL-\d{4}-\d{3})", sqa_content
            )
            if change_log_match:
                return change_log_match.group(1)
        return None

    if pathlib.Path(store).exists():
        data = A_GIS.Data.Json.load_from_db(file=store, leave=False)
    else:
        data = {}

    # Quick return.
    if only_from_store:
        return apply_filters(data, label=label, closed_only=closed_only)

    api_key = os.getenv(api_key_env)

    gl = gitlab.Gitlab(url, private_token=api_key)
    p = gl.projects.get(project_number)

    count = 0
    cached_data = {}
    with tqdm.notebook.tqdm(p.issues.list(iterator=True)) as pbar:
        for f in pbar:
            if not full_update:
                if f.iid in data:
                    if data[f.iid][
                        "updated_at"
                    ] == A_GIS.Time.convert_to_string(time=f.updated_at):
                        pbar.set_postfix({"skip": str(f.iid)})
                        continue
            labelevents = f.resourcelabelevents.list(get_all=True)
            pbar.set_postfix({"get": str(f.iid)})
            
            # Skip if we're filtering by label and this issue doesn't have it
            if label and label not in f.labels:
                continue
                
            # Skip if we're only looking for closed issues and this one isn't closed
            if closed_only and not f.closed_at:
                continue
                
            data[f.iid] = {
                "title": f.title,
                "iid": f.iid,
                "web_url": f.web_url,
                "created_at": A_GIS.Time.convert_to_string(time=f.created_at),
                "closed_at": A_GIS.Time.convert_to_string(time=f.closed_at),
                "started_at": get_started_at(f),
                "labels": f.labels,
                "events": label_times(labelevents),
                "scl": extract_scl(f.description),
                "updated_at": A_GIS.Time.convert_to_string(time=f.updated_at),
            }
            cached_data[f.iid] = data[f.iid]
            count += 1
            if count % save_every == 0:
                A_GIS.Data.Json.save_to_db(
                    data=cached_data, file=store, leave=False
                )
                count = 0
                cached_data = {}

    # Final save to get anything left over.
    A_GIS.Data.Json.save_to_db(data=cached_data, file=store, leave=False)

    # Apply all filters before returning
    return apply_filters(data, label=label, closed_only=closed_only)
