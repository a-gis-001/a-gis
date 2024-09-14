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
        import datetime

        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            if self.logger:
                self.logger.info(f"Event ({event_type}) for file: {file_path}")

            # Check if we should ignore the file
            if self.should_ignore(path=file_path):
                return

            try:
                # Try to get the modification time; skip if the file
                # doesn't exist
                mod_time = os.path.getmtime(file_path)
            except FileNotFoundError:
                # Handle temporary files that are deleted before we can
                # access them
                if self.logger:
                    self.logger.debug(
                        f"File not found or deleted too quickly: {file_path}"
                    )
                return
            mod_time = datetime.datetime.now().timestamp()

            # Calculate SHA-256 checksum
            sha256 = A_GIS.File.hash(file=file_path)

            # Try to find the existing document
            existing_entry = self.collection.find_one({"_id": file_path})

            # Initialize empty lists
            sha256_list = []
            mod_time_list = []
            angle_list = []

            # Calculate the new embedding.
            # If the SHA-256 hasn't changed then we do not update.
            try:
                if existing_entry:
                    sha256_list = existing_entry.get("sha256_list")
                    mod_time_list = existing_entry.get("mod_time_list")
                    angle_list = existing_entry.get("angle_list")
                    if sha256_list[-1] == sha256:
                        if self.logger:
                            self.logger.debug(
                                f"No changes detected in {file_path}, skipping update."
                            )
                        return
                text = A_GIS.File.read_to_text(file=pathlib.Path(file_path))
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
                if logger:
                    self.logger.warning(f"Caught an exception: {e}")
                embedding = None

            # Get the angle from null embedding.
            angle, _ = A_GIS.Math.calculate_angle_between_vectors(
                a=self.null_embedding, b=embedding
            )

            # Update lists with the new values, keeping only some entries.
            sha256_list = update_list_with_limit(
                sha256_list, sha256, self.max_entries
            )
            mod_time_list = update_list_with_limit(
                mod_time_list, mod_time, self.max_entries
            )
            angle_list = update_list_with_limit(
                angle_list, angle, self.max_entries
            )

            # Update or insert the file tracking information
            self.collection.update_one(
                {"_id": file_path},
                {
                    "$set": {
                        "sha256_list": sha256_list,
                        "mod_time_list": mod_time_list,
                        "angle_list": angle_list,
                        "embedding": embedding,
                    }
                },
                upsert=True,  # Insert the document if it doesn't exist
            )

            # Put the result in a queue.
            result = {
                "file_path": file_path,
                "mod_time": mod_time_list[-1],
                "sha256": sha256_list[-1],
                "angle": angle_list[-1],
            }
            if self.logger:
                self.logger.info(f"Added result to queue: {result}")
            self.result_queue.put(result)

    def on_modified(self, event):
        self.process_event(event, "modified")

    def on_created(self, event):
        self.process_event(event, "created")
