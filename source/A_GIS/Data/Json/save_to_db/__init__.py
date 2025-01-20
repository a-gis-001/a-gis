def save_to_db(data, file="data.json", debug=False):
    """Saves a dictionary to a local JSON database file.

    This function takes a dictionary `data` containing key-value pairs
    and saves it into a JSON database stored in a file, which defaults
    to "data.json". The function updates the existing records with new
    values for the given keys or inserts new key-value pairs if they do
    not exist. It supports an optional debug mode that prints out the
    operations being performed.

    Args:
        data (dict):
            A dictionary containing key-value pairs to be saved in the
            database.
        file (str, optional):
            The path to the JSON database file. Defaults to "data.json".
        debug (bool, optional):
            If True, print out the operations being performed for each
            key.

    Returns:
        None:
            This function does not return any value. It updates the
            database in place.
    """
    import tinydb
    import tqdm

    db = tinydb.TinyDB(file)

    # Insert or overwrite data
    for key, value in tqdm.notebook.tqdm(data.items()):
        if db.search(tinydb.Query().key == key):  # Check if the key exists
            db.update({"key": key, "value": value}, Query().key == key)
            if debug:
                print(str(key) + "u", end=",")
        else:
            db.insert({"key": key, "value": value})
            if debug:
                print(str(key) + "n", end=",")

    db.close()
