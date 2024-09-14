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

    def __init__(self, collection, should_ignore, logger, max_entries):
        self.collection = collection
        self.should_ignore = should_ignore
        self.logger = logger
        self.max_entries = max_entries
        self.result_queue = queue.Queue()

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
                current_mod_time = os.path.getmtime(file_path)
            except FileNotFoundError:
                # Handle temporary files that are deleted before we can
                # access them
                if self.logger:
                    self.logger.debug(
                        f"File not found or deleted too quickly: {file_path}"
                    )
                return
            current_mod_time = datetime.datetime.now().timestamp()

            # Calculate SHA-256 checksum
            sha256 = A_GIS.File.hash(file=file_path)

            # Try to find the existing document
            existing_entry = self.collection.find_one({"_id": file_path})

            # If the SHA-256 hasn't changed but there has been an angle change
            # recorded then we skip. This is so you don't keep overwriting history
            # with no real data.
            if existing_entry:
                # Get existing lists or initialize empty lists
                sha256_list = existing_entry.get("sha256_list", [])
                mod_time_list = existing_entry.get("mod_time_list", [])
                angle_list = existing_entry.get("angle_list", [])

                if angle_list[-1] != 0.0 and sha256_list[-1] == sha256:
                    if self.logger:
                        self.logger.debug(
                            f"No changes detected in {file_path}, skipping update."
                        )
                    return

            try:
                text = A_GIS.File.read_to_text(file=pathlib.Path(file_path))
                _, embedding, _ = A_GIS.Text.calculate_embedding(
                    lines=[text], nchunks=1
                )
                embedding = list(embedding.flatten())
            except BaseException as e:
                # Print the exception and its message
                if logger:
                    self.logger.warning(f"Caught an exception: {e}")
                embedding = None

            if embedding is None:
                if logger:
                    self.logger.warning(
                        f"Failed to retrieve embedding for {file_path}"
                    )
                return

            dir = []
            if existing_entry:

                # Get the previous embedding and calculate the angle
                # between the two
                previous_embedding = existing_entry.get("embedding", None)
                previous_dir = existing_entry.get("dir", [])
                if previous_embedding is not None:
                    if len(previous_embedding) != len(embedding):
                        previous_embedding = embedding
                    sign = 1.0
                    if len(previous_dir) == len(embedding):
                        if len(angle_list) > 0 and angle_list[-1] < 0.0:
                            sign = numpy.sign(angle_list[-1])
                    angle_between_embeddings, dir = (
                        A_GIS.Math.calculate_angle_between_vectors(
                            a=previous_embedding,
                            b=embedding,
                            previous_dir=previous_dir,
                            sign=sign,
                        )
                    )
                else:
                    angle_between_embeddings = 0.0
                    dir = list(previous_dir)

            else:
                # Initialize if first time tracking the file
                angle_between_embeddings = 0.0
                sha256_list = []
                mod_time_list = []
                angle_list = []

            # Update lists with the new values, keeping only some entries.
            sha256_list = update_list_with_limit(
                sha256_list, sha256, self.max_entries
            )
            mod_time_list = update_list_with_limit(
                mod_time_list, current_mod_time, self.max_entries
            )
            angle_list = update_list_with_limit(
                angle_list, angle_between_embeddings, self.max_entries
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
                        "dir": dir,
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
