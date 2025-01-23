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
):
    """Gets the raw data to calculate metrics."""
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
        )
    else:
        valid_options = ", ".join(ADAPTER_HANDLERS.keys())
        raise ValueError(
            f"The adapter '{adapter}' is unknown! It should be one of: {valid_options}"
        )

    return data
