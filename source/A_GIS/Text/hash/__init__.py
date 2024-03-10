def hash(*, text: str):
    """Generates a SHA-256 hash of the provided text string and returns it as a hexadecimal digest.

    The function uses the `hashlib` module to generate a SHA-256 hash of the input text, which is then returned as a hexadecimal digest. The input text should be encoded into UTF-8 before hashing, ensuring consistent and correct results across different systems.

    Args:
        text (str): The input string for which to generate a SHA-256 hash.

    Raises:
        None

    Returns:
        str: A hexadecimal digest of the SHA-256 hash of the input text string.
    """

    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
