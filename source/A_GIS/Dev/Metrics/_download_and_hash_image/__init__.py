def _download_and_hash_image(image_info, store_path, leave_progress_bar=False):
    """Download image and calculate its SHA256 hash.

    Args:
        image_info (dict): Dictionary containing image name and URL.
        store_path (pathlib.Path): Base path for storing images.

    Returns:
        dict: Updated image info with local path and hash.
    """
    import hashlib
    import A_GIS.File.download
    import A_GIS.File.make_directory
    import os
    import pathlib
    import shutil

    path = None
    hash = None
    error = None
    try:
        with A_GIS.File.make_directory(scoped_delete=True) as temp_dir:
            filename = pathlib.Path(os.path.basename(image_info["link"]))
            A_GIS.File.download(
                url=image_info["url"],
                output_folder=temp_dir.path,
                filename=filename,
                start_from_scratch=False,
                leave_progress_bar=leave_progress_bar,
            )
            old_filename = temp_dir.path / filename
            hash = A_GIS.File.hash(file=old_filename)
            ext = filename.suffix

            # Create images directory if it doesn't exist and move image there.
            store_dir = pathlib.Path(store_path).parent
            images_dir = store_dir / "images"
            images_dir.mkdir(exist_ok=True)

            new_filename = images_dir / (hash + ext)
            shutil.move(old_filename, new_filename)

            path = str(new_filename.relative_to(store_dir))

    except Exception as e:
        error = str(e)

    return {
        "link": image_info["link"],
        "url": image_info["url"],
        "path": path,
        "hash": hash,
    }, error
