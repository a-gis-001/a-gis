def _detect_mime_from_source(*, source, sniff_bytes: int = 2048) -> str:
    """
    Detects the MIME type of a file path, URL, or file-like object.

    Args:
        source: A string path/URL, Path object, or open file-like object (binary).
        sniff_bytes: Number of bytes to read for magic-based detection.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import urllib.parse
    import A_GIS.Data.Mime._detect_mime_from_filelike
    import A_GIS.Data.Mime._detect_mime_from_url
    import A_GIS.Data.Mime._detect_mime_from_path

    # Handle file-like objects
    if hasattr(source, "read"):
        return A_GIS.Data.Mime._detect_mime_from_filelike(
            source=source, sniff_bytes=sniff_bytes
        )

    source_str = str(source)
    parsed = urllib.parse.urlparse(source_str)

    # URL case
    if parsed.scheme in ("http", "https", "ftp", "file"):
        return A_GIS.Data.Mime._detect_mime_from_url(url=source_str)

    # File path
    return A_GIS.Data.Mime._detect_mime_from_path(path=source_str)
