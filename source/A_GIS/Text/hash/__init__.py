def hash(*, text: str):
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
