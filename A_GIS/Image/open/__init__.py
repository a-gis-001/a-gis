def open(*, path: str):
    """
    Open an image file from the given path.

    This function uses the PIL library to open an image file located at the specified path.

    Args:
        path (str): The path to the image file to be opened.

    Returns:
        PIL.Image.Image: An image object opened from the given path.

    Example:
        >>> image = open(path='path/to/image.jpg')
    """
    from PIL import Image

    # Open and return the image located at the specified path
    return Image.open(path)
