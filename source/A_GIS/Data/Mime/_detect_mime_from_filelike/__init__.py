def _detect_mime_from_filelike(*, source, sniff_bytes: int = 2048) -> str:
    """
    Detects the MIME type of a file-like object by reading its contents.

    Args:
        source: An open file-like object (binary).
        sniff_bytes: Number of bytes to read for magic-based detection.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import A_GIS.Data.Mime._detect_mime_type

    if not hasattr(source, "read"):
        raise ValueError(
            "Source must be a file-like object with a read method"
        )

    pos = (
        source.tell()
        if hasattr(source, "seek") and source.seekable()
        else None
    )
    head = source.read(sniff_bytes)
    if pos is not None:
        source.seek(pos)
    return A_GIS.Data.Mime._detect_mime_type(data=head)
