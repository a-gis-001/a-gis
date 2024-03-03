import PIL.Image


def remove(*, image: PIL.Image.Image) -> PIL.Image.Image:
    """
    Generate a purified copy of a given image for consistent hashing.

    This function creates a 'pure' version of the input image by removing any additional metadata
    and retaining only the essential visual data. It's particularly useful for consistent hashing
    of image data, ensuring the hash is based solely on the image's visual content.

    Args:
        image (PIL.Image.Image): The image object to be purified. Must be a PIL Image object.
        custom_new (Optional[Callable[..., PIL.Image.Image]]): An optional custom function to create a new image object.
                                                              If None, `PIL.Image.new` is used as the default.

    Returns:
        PIL.Image.Image: A purified copy of the input image. This includes the same visual content
                        and color palette (if applicable), but without any additional metadata.

    Raises:
        ValueError: If `image` is not a PIL Image object.

    Note:
        The function ensures that the returned image is devoid of metadata like EXIF data,
        which can affect hash consistency.
    """

    if not isinstance(image, PIL.Image.Image):
        raise ValueError("Invalid image type. Expected a PIL Image object.")

    # Create a new image with the same mode and size as the original
    pure_image = PIL.Image.new(mode=image.mode, size=image.size)

    # Transfer pixel data from the original image to the new image
    pure_image.putdata(list(image.getdata()))

    # If the original image has a color palette, copy it to the new image
    if "P" in image.mode and hasattr(image, "getpalette"):
        pure_image.putpalette(image.getpalette())

    return pure_image
