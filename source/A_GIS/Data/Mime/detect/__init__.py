def detect(*, data_or_source, sniff_bytes: int = 2048):
    """
    Detects the MIME type of binary data, a file path, URL, or file-like object.

    Args:
        data_or_source: Binary data, a string path/URL, Path object, or open file-like object.
        sniff_bytes: Number of bytes to read for magic-based detection.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import typing
    import pathlib
    import A_GIS.Data.Mime._detect_mime_type
    import A_GIS.Data.Mime._detect_mime_from_source

    # If it's binary data
    if isinstance(data_or_source, bytes):
        return A_GIS.Data.Mime._detect_mime_type._detect_mime_type(
            data=data_or_source
        )

    # Handle everything else as a source
    return A_GIS.Data.Mime._detect_mime_from_source._detect_mime_from_source(
        source=data_or_source, sniff_bytes=sniff_bytes
    )
