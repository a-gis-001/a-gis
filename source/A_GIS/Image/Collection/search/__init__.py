def search(*, collection, encodings, topk=32, nprobe=16, nlist=1024):
    import numpy

    search_vectors = [numpy.asarray(x.cpu()) for x in encodings]

    # Create an index.
    _METRIC_TYPE = "L2"
    _INDEX_TYPE = "IVF_FLAT"
    index_param = {
        "index_type": _INDEX_TYPE,
        "params": {"nlist": nlist},
        "metric_type": _METRIC_TYPE,
    }
    collection.db.create_index(collection.vec["name"], index_param)

    # Search the index.
    search_param = {
        "data": search_vectors,
        "anns_field": collection.vec["name"],
        "param": {"metric_type": _METRIC_TYPE, "params": {"nprobe": nprobe}},
        "limit": topk,
    }

    collection.db.load()
    return collection.db.search(**search_param)
