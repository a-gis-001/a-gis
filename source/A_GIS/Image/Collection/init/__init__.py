def init(
    *,
    base_dir="__a_gis_image_db__",
    host="127.0.0.1",
    port=19530,
    name="image_db",
    id={"length": 256, "description": "filename", "name": "id"},
    vec={"dim": 512, "description": "encoding", "name": "vec"},
    album={"length": 256, "description": "name of album", "name": "album"},
):
    """Initialize a collection of images using a vector database.

    This function initializes a new collection within a Milvus vector database,
    allowing for the storage and retrieval of image data along with their associated vectors and metadata. The collection is configured with user-defined parameters for file storage paths, server connection details, and schema definitions for the data fields.

    Args:
        base_dir (str, optional):
            The base directory where the Milvus server stores its data. Default is `__a_gis_image_db__`.
        host (str, optional):
            The host address of the Milvus server. Default is `127.0.0.1`.
        port (int, optional):
            The network port on which the Milvus server listens for connections. Default is `19530`.
        name (str):
            The name of the collection to be created within the Milvus database.
        id (dict):
            Configuration for the 'id' field in the collection schema. It specifies the field's length, description, and whether it is a primary key. Example: `{'length': 256, 'description': 'filename', 'name': 'id'}`.
        vec (dict):
            Configuration for the 'vec' field in the collection schema. It defines the field's data type (FLOAT_VECTOR), dimension, description, and whether it is a primary key. Example: `{'dim': 512, 'description': 'encoding', 'name': 'vec'}`.
        album (str):
            Configuration for the 'album' field in the collection schema. It specifies the field's data type (VARCHAR), maximum length, description, and whether it is a primary key. Example: `{'length': 256, 'description': 'name of album', 'name': 'album'}`.

    Returns:
        _Collection:
            An instance of the dataclass `_Collection` containing the initialization parameters for the Milvus collection, along with the connection details and schema.

    Raises:
        Exception:
            If the Milvus server cannot be connected to on the specified host and port, an exception will be raised. The function will attempt to start the Milvus server locally if it is not already running. If the server still cannot be connected to after these attempts, `None` is returned, and an error message is printed.
    """

    import milvus
    import pymilvus
    import dataclasses
    import typing

    # Optional, if you want store all related data to specific location
    # default it wil using %APPDATA%/milvus-io/milvus-server
    milvus.default_server.set_base_dir(base_dir)

    # Connect to Milvus server
    try:
        pymilvus.connections.connect(host=host, port=port)
        print("Connected to Milvus server at {}:{}".format(host, port))
    except Exception as e:
        milvus.default_server.start()
        try:
            pymilvus.connections.connect(host=host, port=port)
            print("Connected to Milvus server at {}:{}".format(host, port))
        except Exception as e:
            print(f"Failed to connect to Milvus server: {e}")
            return None

    # Create.
    field1 = pymilvus.FieldSchema(
        name=id["name"],
        dtype=pymilvus.DataType.VARCHAR,
        max_length=id["length"],
        description=id["description"],
        is_primary=True,
    )
    field2 = pymilvus.FieldSchema(
        name=vec["name"],
        dtype=pymilvus.DataType.FLOAT_VECTOR,
        description="float vector",
        dim=vec["dim"],
        is_primary=False,
    )
    field3 = pymilvus.FieldSchema(
        name=album["name"],
        dtype=pymilvus.DataType.VARCHAR,
        max_length=album["length"],
        description=album["description"],
        is_primary=False,
    )
    schema = pymilvus.CollectionSchema(
        fields=[field1, field2], description="collection description"
    )
    db = pymilvus.Collection(
        name=name,
        data=None,
        schema=schema,
        properties={"collection.ttl.seconds": 15},
    )

    @dataclasses.dataclass
    class _Collection:
        base_dir: str
        host: str
        name: str
        port: int
        id: dict
        vec: dict
        album: str
        db: typing.Any

    return _Collection(
        base_dir=base_dir,
        host=host,
        name=name,
        port=port,
        id=id,
        vec=vec,
        album=album,
        db=db,
    )
