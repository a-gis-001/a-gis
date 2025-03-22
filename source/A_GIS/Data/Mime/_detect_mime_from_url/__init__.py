def _detect_mime_from_url(*, url: str) -> str:
    """
    Detects the MIME type of a URL by examining its file extension.

    Args:
        url: A URL string (http, https, ftp, or file protocol).

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import mimetypes
    import urllib.parse

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https", "ftp", "file"):
        raise ValueError("URL must use http, https, ftp, or file protocol")
    
    return mimetypes.guess_type(parsed.path)[0] 