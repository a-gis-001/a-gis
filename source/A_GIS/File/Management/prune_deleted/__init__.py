def prune_deleted(*, collection, sha256=None, logger=None):
    """Remove MongoDB entries for non-existent files.

    This function updates a MongoDB collection by removing entries where
    the associated file does not exist on the filesystem. It accepts
    optional parameters for specifying the collection, a SHA-256 hash to
    filter documents, and a logger instance for informational messages.

    Args:
        collection (pymongo.collection.Collection):
            The MongoDB collection from which to remove deleted file
            entries.
        sha256 (str, optional):
            A specific SHA-256 hash to filter the documents to be
            pruned. If None, all documents are considered.
        logger (logging.Logger, optional):
            An optional logger instance for informational messages.
            Defaults to None.

    Returns:
        :
            list of str: A list of file paths that were removed from the
            database as they no longer exist on the filesystem.
    """
    import os

    # Find all documents where 'sha256_list' contains the given sha256
    if sha256:
        cursor = collection.find({"sha256_list": sha256})
    else:
        cursor = collection.find()

    deleted = []
    for doc in cursor:
        file_path = doc["_id"]  # Assuming '_id' is the file_path

        # Check if the file exists on the filesystem
        if not os.path.exists(file_path):
            # Remove the document from the collection
            collection.delete_one({"_id": file_path})
            deleted.append(file_path)
            if logger:
                logger.info(
                    f"Removed database entry for non-existent file: {file_path}"
                )
    return deleted
