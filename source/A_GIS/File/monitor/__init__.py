def monitor(
    *,
    root_dir: type["pathlib.Path"],
    ignore_dirs: list = [],
    ignore_subdirs: list = [],
    only_extensions=[],
    ignore_dot_files=True,
    database_name: str = "file_monitor",
    collection_name: str = "file_changes",
    debug=True,
    sleep_seconds=1,
    max_entries=32,
):
    """Monitor a list of directories for changes

    Stores changes in a mongodb.

    """
    import os
    import time
    import pymongo
    import watchdog.observers
    import watchdog.events
    import sys
    import A_GIS.File.hash
    import math
    import numpy
    import pathlib
    import queue

    # MongoDB setup
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[database_name]  # Database
    collection = db[collection_name]  # Collection

    result_queue = queue.Queue()

    # Function to ensure lists are capped at max_entries
    def update_list_with_limit(lst, new_item, limit=max_entries):
        lst.append(new_item)
        if len(lst) > limit:
            lst = lst[-limit:]  # Keep only the latest `limit` items
        return lst

    # Watchdog event handler for file changes
    class FileModificationHandler(watchdog.events.FileSystemEventHandler):
        def __init__(
            self,
            ignore_dirs,
            ignore_subdirs,
            only_extensions,
            ignore_dot_files,
        ):
            self.ignore_dirs = ignore_dirs
            self.ignore_subdirs = ignore_subdirs
            self.only_extensions = set(only_extensions)
            self.ignore_dot_files = ignore_dot_files

        def on_modified(self, event):
            if not event.is_directory:
                file_path = os.path.abspath(event.src_path)
                if debug:
                    print(f"Event for file: {file_path}")

                # Only consider certain extensions.
                if self.only_extensions:
                    ext = os.path.splitext(file_path)[1]
                    if not ext in self.only_extensions:
                        if debug:
                            print(
                                f"Ignored because not in extension list: {file_path}"
                            )
                        return

                # Ignore file changes inside specific directories or files
                # starting with "."
                if self.ignore_dot_files and any(
                    part.startswith(".") for part in file_path.split(os.sep)
                ):
                    if debug:
                        print(f"Ignored hidden file or directory: {file_path}")
                    return

                # Ignore file changes inside specific directories
                for ignored_dir in self.ignore_dirs:
                    if file_path.startswith(os.path.abspath(ignored_dir)):
                        if debug:
                            print(f"Ignored change in: {file_path}")
                        return

                # Ignore file changes inside specific named subdirectories
                dirs = set(file_path.split(os.sep)[:-2])
                for ignored_subdir in self.ignore_subdirs:
                    if ignored_subdir in dirs:
                        if debug:
                            print(
                                f"Ignored subdir {ignored_subdir} change in: {file_path}"
                            )
                        return

                try:
                    # Try to get the modification time; skip if the file
                    # doesn't exist
                    current_mod_time = os.path.getmtime(file_path)
                except FileNotFoundError:
                    # Handle temporary files that are deleted before we can
                    # access them
                    if debug:
                        print(
                            f"File not found or deleted too quickly: {file_path}"
                        )
                    return
                # Calculate SHA-256 checksum
                sha256 = A_GIS.File.hash(file=file_path)

                # Try to find the existing document
                existing_entry = collection.find_one({"_id": file_path})

                # If the SHA-256 hasn't changed, skip the update
                if (
                    existing_entry
                    and existing_entry.get("sha256_list", [])
                    and existing_entry["sha256_list"][-1] == sha256
                ):
                    if debug:
                        print(
                            f"No changes detected in {file_path}, skipping update."
                        )
                    return

                try:
                    text = A_GIS.File.read_to_text(
                        file=pathlib.Path(file_path)
                    )
                    _, embedding, _ = A_GIS.Text.calculate_embedding(
                        lines=[text], nchunks=1
                    )
                    embedding = list(embedding.flatten())
                except BaseException:
                    embedding = None

                if embedding is None:
                    if debug:
                        print(f"Failed to retrieve embedding for {file_path}")
                    return

                dir = []
                if existing_entry:
                    # Get existing lists or initialize empty lists
                    sha256_list = existing_entry.get("sha256_list", [])
                    mod_time_list = existing_entry.get("mod_time_list", [])
                    angle_list = existing_entry.get("angle_list", [])

                    # Get the previous embedding and calculate the angle
                    # between the two
                    previous_embedding = existing_entry.get("embedding", None)
                    previous_dir = existing_entry.get("dir", [])
                    if previous_embedding is not None:
                        if len(previous_embedding) != len(embedding):
                            previous_embedding = embedding
                        sign = 1.0
                        if len(previous_dir) == len(embedding):
                            if len(angle_list) > 0:
                                if angle_list[-1] < 0.0:
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

                # Update lists with the new values, keeping only the last 32
                # entries
                sha256_list = update_list_with_limit(sha256_list, sha256)
                mod_time_list = update_list_with_limit(
                    mod_time_list, current_mod_time
                )
                angle_list = update_list_with_limit(
                    angle_list, angle_between_embeddings
                )

                # Update or insert the file tracking information
                collection.update_one(
                    {"_id": file_path},
                    {
                        "$set": {
                            "sha256_list": sha256_list,  # Store the checksum list
                            "mod_time_list": mod_time_list,  # Store the modification time list
                            "angle_list": angle_list,  # Store the angle list
                            "embedding": embedding,  # Store the current embedding
                            "dir": dir,
                        }
                    },
                    upsert=True,  # Insert the document if it doesn't exist
                )

                # Yield the data as an iterator
                result_queue.put(
                    {
                        "file_path": file_path,
                        "mod_time": mod_time_list[-1],
                        "sha256": sha256_list[-1],
                        "angle": angle_list[-1],
                    }
                )

    event_handler = FileModificationHandler(
        ignore_dirs, ignore_subdirs, only_extensions, ignore_dot_files
    )
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, root_dir, recursive=True)
    observer.start()

    try:
        while True:
            while not result_queue.empty():
                yield result_queue.get()
            time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
