def process_images(
    *, issue, attachment_url, store_path, download=False, use_cache=True
):
    """Process images in issue.

    Args:
        issue (gitlab.v4.objects.Issue): GitLab issue object.
        attachment_url (str): Base GitLab URL.
        store_path (pathlib.Path): Path to data store.
        download (bool, optional): Whether to download images. Defaults to False.

    Returns:
        list: List of image information dictionaries.
    """
    import A_GIS.Dev.Metrics._extract_image_urls
    import A_GIS.Dev.Metrics._download_and_hash_image
    import A_GIS.Data.Format.Json.load_from_db
    import pathlib

    images = A_GIS.Dev.Metrics._extract_image_urls(issue, attachment_url)
    errors = []

    if download and images:
        already_have = {}
        if use_cache:
            data = A_GIS.Data.Format.Json.load_from_db(
                file=store_path, leave=False, only_keys=[issue.iid]
            )
            if issue.iid in data:
                for i in data[issue.iid]["images"]:
                    if i["hash"] and i["path"]:
                        hash_value = A_GIS.File.hash(
                            file=(pathlib.Path(store_path).parent) / i["path"]
                        )
                        if i["hash"] == hash_value:
                            already_have[i["link"]] = i
        local_images = []
        for image in images:
            if image["link"] in already_have:
                local_images.append(already_have[image["link"]])
                errors.append(None)
            else:
                image_info, error = A_GIS.Dev.Metrics._download_and_hash_image(
                    image, store_path
                )
                local_images.append(image_info)
                errors.append(error)
        images = local_images

    return images, errors
