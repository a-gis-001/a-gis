def process_images(issue, base_url, store_path, *, download=False):
    """Process images in issue.

    Args:
        issue (gitlab.v4.objects.Issue): GitLab issue object.
        base_url (str): Base GitLab URL.
        store_path (pathlib.Path): Path to data store.
        download (bool, optional): Whether to download images. Defaults to False.

    Returns:
        list: List of image information dictionaries.
    """
    import A_GIS.Dev.Metrics._extract_image_urls
    import A_GIS.Dev.Metrics._download_and_hash_image

    images = A_GIS.Dev.Metrics._extract_image_urls(issue, base_url)
    if download and images:
        return [
            A_GIS.Dev.Metrics._download_and_hash_image(img, store_path)
            for img in images
        ]
    return images
