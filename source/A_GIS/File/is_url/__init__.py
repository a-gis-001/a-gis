def is_url(name: str):
    """Checks if a given name is a URL with a recognized protocol scheme.

    This function uses the `urlparse` method from the `urllib.parse` module to parse
    the input name into its components, and checks if it has a recognized protocol
    scheme (http, https, ftp or ftps). If both conditions are met, the function
    returns True; otherwise, False.

    Args:
        name (str): The name to be checked.

    Returns:
        bool: True if the name is a URL with a recognized protocol scheme,
              False otherwise.
    """

    import urllib

    parsed_name = urllib.parse.urlparse(str(name))
    return bool(parsed_name.scheme) and parsed_name.scheme in [
        "http",
        "https",
        "ftp",
        "ftps",
    ]
