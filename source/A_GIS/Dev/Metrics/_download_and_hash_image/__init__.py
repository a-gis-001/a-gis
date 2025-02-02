def _download_and_hash_image(image_info, store_path):
    """Download image and calculate its SHA256 hash.

    Args:
        image_info (dict): Dictionary containing image name and URL.
        store_path (pathlib.Path): Base path for storing images.

    Returns:
        dict: Updated image info with local path and hash.
    """
    import hashlib
    import A_GIS.File.download

    try:
        # Create images directory if it doesn't exist
        images_dir = store_path.parent / "images"
        images_dir.mkdir(exist_ok=True)

        # Generate filename from name and URL
        url_hash = hashlib.sha256(image_info["url"].encode()).hexdigest()[:8]
        filename = f"{image_info['name']}_{url_hash}"
        local_path = images_dir / filename

        # Download the image
        A_GIS.File.download(
            url=image_info["url"],
            output_folder=images_dir,
            filename=filename,
            start_from_scratch=False,
        )

        # Calculate SHA256
        sha256 = hashlib.sha256()
        with open(local_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        return {
            "name": image_info["name"],
            "url": image_info["url"],
            "local_path": str(local_path.relative_to(store_path.parent)),
            "sha256": sha256.hexdigest(),
        }
    except Exception as e:
        print(f"Error downloading {image_info['url']}: {str(e)}")
        return {
            "name": image_info["name"],
            "url": image_info["url"],
            "error": str(e)
        }
