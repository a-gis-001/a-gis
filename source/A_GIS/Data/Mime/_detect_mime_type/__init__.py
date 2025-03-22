def _detect_mime_type(*, data: bytes) -> str:
    """
    Detects the MIME type of binary data.

    Args:
        data: Binary data to analyze.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import magic

    # Handle empty data
    if not data:
        return None

    try:
        return magic.from_buffer(data, mime=True)
    except Exception:
        return None
