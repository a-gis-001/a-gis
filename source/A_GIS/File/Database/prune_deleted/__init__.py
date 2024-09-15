def prune_deleted(*, collection, sha256, logger=None):
    """Prune from the collection any non-existent files matching sha256.

    Args:
        collection (Collection): The MongoDB collection instance.
        sha256 (str): The SHA-256 hash to match files against.

    Returns:
        None
    """
    import os

    # Find all documents where 'sha256_list' contains the given sha256
    cursor = collection.find({"sha256_list": sha256})

    for doc in cursor:
        file_path = doc["_id"]  # Assuming '_id' is the file_path

        # Check if the file exists on the filesystem
        if not os.path.exists(file_path):
            # Remove the document from the collection
            collection.delete_one({"_id": file_path})
            if logger:
                logger.info(
                    f"Removed database entry for non-existent file: {file_path}"
                )
