def open(*, path: str):
    """
    Open an image file from either a local file path or a URL.

    This function uses the PIL library to open a local image file, and the requests library
    to fetch and open an image from a URL.

    Args:
        source (str): The path or URL of the image to be opened.

    Returns:
        PIL.Image.Image: An image object opened from the given path or URL.

    Example:
        >>> import A_GIS.Image
        >>> image = A_GIS.Image.open(path='https://picsum.photos/200')
    """
    from PIL import Image
    from io import BytesIO
    import requests

    # Check if the source is a URL
    if path.startswith("http://") or path.startswith("https://"):
        # Fetch the image from the URL
        response = requests.get(path)
        response.raise_for_status()  # This will raise an exception for HTTP errors

        # Open and return the image from the response content
        return Image.open(BytesIO(response.content))
    else:
        # Open and return the image from a local file
        return Image.open(path)
