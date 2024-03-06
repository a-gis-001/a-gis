def is_url(path):
    from urllib.parse import urlparse

    parsed_path = urlparse(str(path))
    return bool(parsed_path.scheme) and parsed_path.scheme in [
        "http",
        "https",
        "ftp",
        "ftps",
    ]
