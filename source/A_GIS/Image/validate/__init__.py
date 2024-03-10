def validate(image: type['PIL.Image.Image']):
    """Checks the provided image for A_GIS standards

    This function checks whether an image object has any associated metadata.
    If there's no metadata, a `ValueError` is raised with a custom message.

    Args:
        image (PIL.Image.Image): The image to be validated.

    Raises:
        ValueError: If the provided image does not have any metadata attached.

    Returns:
        None
    """

    if not hasattr(image, "info") or image.info is None:
        raise ValueError("image must have metadata!")
    pass
