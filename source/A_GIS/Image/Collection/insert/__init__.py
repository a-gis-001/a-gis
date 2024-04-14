def insert(*, collection, ids, encodings):
    import numpy

    # Require length of ids and encodings are the same
    data = [[str(x) for x in ids], [numpy.asarray(x.cpu()) for x in encodings]]
    collection.db.insert(data)
    return collection
