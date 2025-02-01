def get_raw_data(
    *,
    url,
    project_number,
    adapter="gitlab_sqa",
    api_key_env="GITLAB_API_KEY",
    store="data.json",
    only_from_store=False,
    save_every=15,
    full_update=False,
    label=None,
    closed_only=False,
):
    """Gets the raw data to calculate metrics.
    
    Args:
        url (str): The GitLab URL.
        project_number (int): The GitLab project number.
        adapter (str, optional): The adapter to use. Defaults to "gitlab_sqa".
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
    import A_GIS.Dev.Metrics._get_raw_data_gitlab_sqa
    import pathlib

    data = None

    # Define a mapping of adapters to their handling functions
    ADAPTER_HANDLERS = {
        "gitlab_sqa": A_GIS.Dev.Metrics._get_raw_data_gitlab_sqa,
    }

    # Get the handler for the provided adapter
    handler = ADAPTER_HANDLERS.get(adapter)

    if handler:
        data = handler(
            url=url,
            project_number=project_number,
            api_key_env=api_key_env,
            store=store,
            only_from_store=only_from_store,
            save_every=save_every,
            full_update=full_update,
            label=label,
            closed_only=closed_only,
        )
    else:
        valid_options = ", ".join(ADAPTER_HANDLERS.keys())
        raise ValueError(
            f"The adapter '{adapter}' is unknown! It should be one of: {valid_options}"
        )

    return data
