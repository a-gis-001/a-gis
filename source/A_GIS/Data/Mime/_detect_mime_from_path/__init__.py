def _detect_mime_from_path(*, path: str) -> str:
    """
    Detects the MIME type of a file path using magic numbers or file extension.

    Args:
        path: A string path or Path object pointing to a file.

    Returns:
        A MIME type string (e.g., 'application/pdf'), or None if detection fails.
    """
    import pathlib
    import mimetypes

    path_obj = pathlib.Path(path)
    if not path_obj.is_file():
        raise ValueError(f"Path does not point to a file: {path}")

    try:
        import magic
        return magic.from_file(str(path_obj), mime=True)
    except Exception:
        return mimetypes.guess_type(path_obj.name)[0] 