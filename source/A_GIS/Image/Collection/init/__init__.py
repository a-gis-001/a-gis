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
