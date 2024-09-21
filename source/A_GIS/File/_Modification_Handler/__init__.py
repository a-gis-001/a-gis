import watchdog.events

class _Modification_Handler(watchdog.events.FileSystemEventHandler):
    """Watchdog event handler for file changes"""

    @staticmethod
    def update_list_with_limit(lst, new_item, limit):
        """Function to ensure lists are capped at limit"""
        lst.append(new_item)
        if len(lst) > limit:
            lst = lst[-limit:]  # Keep only the latest `limit` items
        return lst

    def __init__(
        self, collection, should_ignore, logger, max_entries, min_bytes
    ):
        import A_GIS.Text.calculate_embedding
        import queue

        self.null_embedding = A_GIS.Text.calculate_embedding(
            lines=[""], nchunks=1
        )[1].flatten()
        self.collection = collection
        self.should_ignore = should_ignore
        self.logger = logger
        self.max_entries = max_entries
        self.result_queue = queue.Queue()
        self.min_bytes = min_bytes

    def process_event(self, event, event_type):
        """Process the file event and update the database."""
        import os
        import A_GIS.File.hash
        import A_GIS.File.read_to_text
        import A_GIS.Text.calculate_embedding
        import A_GIS.Math.calculate_angle_between_vectors
        import A_GIS.File.Database.prune_deleted
        import datetime
        import pathlib

        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            if self.logger:
                self.logger.info(f"Event ({event_type}) for file: {file_path}")

            # Check if we should ignore the file
            if self.should_ignore(path=file_path):
                return

            # Try to get properties like modification time and size.
            updates = {"file_path": file_path}
            try:
                updates["bytes"] = os.path.getsize(file_path)
            except FileNotFoundError:
                # We come here typically for temporary files that are deleted before we can
                # access them.
                if self.logger:
                    self.logger.debug(
                        f"File not found or deleted too quickly: {file_path}"
                    )
                return
            updates["mod_time"] = datetime.datetime.now().timestamp()

            # Check if too small to track.
            if updates["bytes"] < self.min_bytes:
                if self.logger:
                    self.logger.info(
                        f"File too small {updates['bytes']}<{self.min_bytes} (bytes): {file_path}"
                    )
                return

            # Calculate SHA-256 checksum
            updates["sha256"] = A_GIS.File.hash(file=file_path)

            # Try to find the existing document
            existing_entry = self.collection.find_one({"_id": file_path})

            # Initialize empty lists
            lists = {"sha256": [], "mod_time": [], "angle": [], "bytes": []}

            # Calculate the new embedding.
            # If the SHA-256 hasn't changed then we do not update.
            try:
                A_GIS.File.Database.prune_deleted(
                    collection=self.collection,
                    sha256=updates["sha256"],
                    logger=self.logger,
                )
                if existing_entry:
                    lists["sha256"] = existing_entry.get("sha256_list", [])
                    lists["mod_time"] = existing_entry.get("mod_time_list", [])
                    lists["angle"] = existing_entry.get("angle_list", [])
                    lists["bytes"] = existing_entry.get("bytes_list", [])
                    if lists["sha256"][-1] == updates["sha256"]:
                        if self.logger:
                            self.logger.debug(
                                f"No changes detected in {file_path}, skipping update."
                            )
                        return

                text = A_GIS.File.read_to_text(
                    path=pathlib.Path(file_path)
                ).text
                _, embedding, _ = A_GIS.Text.calculate_embedding(
                    lines=[text], nchunks=1
                )
                embedding = list(embedding.flatten())
                if len(self.null_embedding) != len(embedding):
                    if self.logger:
                        self.logger.warning(
                            f"Embedding for {file_path} inconsistent size compared to null embedding. Probably you have changed embeddings and are using an old database."
                        )
                    return

            except BaseException as e:
                # Print the exception and its message
                if self.logger:
                    self.logger.warning(f"Caught an exception: {e}")
                embedding = None

            # Get the angle from null embedding.
            if embedding:
                updates["angle"], _ = (
                    A_GIS.Math.calculate_angle_between_vectors(
                        a=self.null_embedding, b=embedding
                    )
                )
            else:
                updates["angle"] = 0

            # Update lists with the new values, keeping only some entries.
            for k, v in lists.items():
                lists[k] = self.update_list_with_limit(
                    v, updates[k], self.max_entries
                )

            # Update or insert the file tracking information
            self.collection.update_one(
                {"_id": file_path},
                {
                    "$set": {
                        "sha256_list": lists["sha256"],
                        "mod_time_list": lists["mod_time"],
                        "angle_list": lists["angle"],
                        "bytes": lists["bytes"],
                        "embedding": embedding,
                    }
                },
                upsert=True,  # Insert the document if it doesn't exist
            )

            # Put the result in a queue.
            if self.logger:
                self.logger.info(f"Added result to queue: {updates}")
            self.result_queue.put(updates)

    def on_modified(self, event):
        self.process_event(event, "modified")

    def on_created(self, event):
        self.process_event(event, "created")
