def _detect_mime_from_source(*, source, sniff_bytes: int = 2048) -> str:
    """
    Detects the MIME type of a file path, URL, or file-like object.

    Args:
        source: A string path/URL, Path object, or open file-like object (binary).
        sniff_bytes: Number of bytes to read for magic-based detection.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import mimetypes
    import urllib.parse
    import pathlib
    import typing
    import A_GIS.Data.Mime._detect_mime_type

    # Handle file-like objects
    if hasattr(source, "read"):
        pos = (
            source.tell()
            if hasattr(source, "seek") and source.seekable()
            else None
        )
        head = source.read(sniff_bytes)
        if pos is not None:
            source.seek(pos)
        return A_GIS.Data.Mime._detect_mime_type._detect_mime_type(data=head)

    source_str = str(source)
    parsed = urllib.parse.urlparse(source_str)

    # URL case — use file extension only
    if parsed.scheme in ("http", "https", "ftp", "file"):
        return mimetypes.guess_type(parsed.path)[0]

    # File path
    path = pathlib.Path(source_str)
    if path.is_file():
        try:
            import magic

            return magic.from_file(str(path), mime=True)
        except Exception:
            return mimetypes.guess_type(path.name)[0]

    # Fallback
    return mimetypes.guess_type(path.name)[0]
