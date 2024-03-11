def is_url(path):
    """Checks if a given path is a URL with a recognized protocol scheme.

    This function uses the `urlparse` method from the `urllib.parse` module to parse
    the input path into its components, and checks if it has a recognized protocol
    scheme (http, https, ftp or ftps). If both conditions are met, the function
    returns True; otherwise, False.

    Args:
        path (str): The path to be checked.

    Raises:
        None

    Returns:
        bool: True if the path is a URL with a recognized protocol scheme,
              False otherwise.
    """

    from urllib.parse import urlparse

    parsed_path = urlparse(str(path))
    return bool(parsed_path.scheme) and parsed_path.scheme in [
        "http",
        "https",
        "ftp",
        "ftps",
    ]
