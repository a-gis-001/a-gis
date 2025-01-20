def load(data={}, file="data.json", debug=False):
    """Read data from a JSON file into a Python dictionary.

    This function reads data from a specified JSON database file and
    loads it into a Python dictionary, making the data accessible for
    further processing or analysis. The database is accessed using the
    `tinydb` library, and the progress can be tracked with `tqdm` if set
    to verbose mode (`debug=True`).

    Args:
        data (dict, optional):
            A dictionary that will be populated with the contents of the
            database. If no argument is provided, a new dictionary will
            be created.
        file (str, optional):
            The path to the JSON database file from which to load the
            data. Defaults to "data.json".
        debug (bool, optional):
            A flag that, when set to True, enables progress tracking via
            `tqdm` and prints out each key-value pair to the console as
            it is loaded into the dictionary.

    Returns:
        dict:
            The data from the database file loaded into a Python
            dictionary with keys corresponding to the record "keys" and
            values corresponding to the associated "values" in the
            database.
    """
    import tinydb
    import tqdm.notebook

    db = tinydb.TinyDB(file)
    for record in tqdm.notebook.tqdm(db.all()):
        if debug:
            print(record["key"], end=",")
        data[record["key"]] = record["value"]
    db.close()
    return data
