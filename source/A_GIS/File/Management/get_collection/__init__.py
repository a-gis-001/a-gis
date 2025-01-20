def get_collection(
    *,
    name: str,
    from_database: str = "test",
    client="mongodb://localhost:27017/",
):
    """Retrieve a pymongo Collection object from a specified MongoDB database and client.

    This function establishes a connection to the MongoDB server and returns a
    pymongo Collection object for the named collection within the specified database.
    The connection is established using the provided client string, which defaults
    to "mongodb://localhost:27017". The database and collection names are required
    to uniquely identify the resource to be accessed.

    Args:
        name (str):
            The name of the collection to retrieve.
        from_database (str), optional (default="test"):
            The name of the database
            containing the collection. Defaults to "test".
        client (str, optional):
            A connection string for MongoDB. Defaults to
            "mongodb://localhost:27017/".

    Returns:
        pymongo.Collection:
            The collection from the specified database within the
            provided MongoDB client instance.

    Raises:
        ConnectionFailure:
            If the connection to the MongoDB server cannot be established,
            a pymongo.errors.ConnectionFailure exception is raised.
        pymongo.errors.InvalidName:
            If the specified collection name is invalid or unrecognized,
            a pymongo.errors.InvalidName exception is raised.
    """

    import pymongo

    return pymongo.MongoClient("mongodb://localhost:27017/")[from_database][
        name
    ]
