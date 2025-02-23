def save_to_db(*, data, file="data.json", leave=True):
    """Saves a dictionary to a local JSON database file.

    This function takes a dictionary `data` containing key-value pairs
    and saves it into a JSON database stored in a file, which defaults
    to "data.json". The function updates the existing records with new
    values for the given keys or inserts new key-value pairs if they do
    not exist.

    Args:
        data (dict):
            A dictionary containing key-value pairs to be saved in the
            database.
        file (str, optional):
            The path to the JSON database file. Defaults to "data.json".

    Returns:
        None:
            This function does not return any value. It updates the
            database in place.
    """
    import tinydb
    import tqdm

    db = tinydb.TinyDB(file)

    # Insert or overwrite data
    with tqdm.notebook.tqdm(data.items(), leave=leave) as pbar:
        for key, value in pbar:
            if db.search(tinydb.Query().key == key):  # Check if the key exists
                db.update(
                    {"key": key, "value": value}, tinydb.Query().key == key
                )
                pbar.set_postfix({"update": str(key)})
            else:
                db.insert({"key": key, "value": value})
                pbar.set_postfix({"insert": str(key)})

    db.close()
