import PIL.Image
import typing


def new(
    *,
    mode: str = "RGBA",
    size: typing.Tuple[int, int] = (0, 0),
    metadata: typing.Optional[typing.Dict[str, str]] = None
) -> PIL.Image.Image:
    """
    Create and return a new image with the specified mode, size, and optional metadata.

    This function utilizes the Python Imaging Library (PIL) to create a new image object.
    The mode specifies the color format, such as 'RGB' or 'RGBA'. The size is defined by a tuple
    (width, height). If metadata is provided, it is added to the image as a dictionary of JSON strings.

    Args:
        mode: The color mode to use for the new image. Defaults to 'RGBA'.
        size: A tuple (width, height) specifying the dimensions of the new image. Defaults to (0, 0).
        metadata: Optional dictionary containing metadata for the image. Each key-value pair is added
                  as a JSON-formatted string. Defaults to None.

    Returns:
        A new PIL.Image.Image object with the specified properties.

    Examples:
        >>> new_image = new(mode='RGB', size=(200, 200), metadata={'Author': 'John Doe', 'Description': 'Sample Image'})
        >>> empty_image = new()

    Raises:
        ImportError: If PIL modules are not available.
    """
    import json  # Import json for metadata serialization
    import PIL.PngImagePlugin  # Import PIL.PngImagePlugin for metadata handling in PNG images

    # Create a new image object with the specified mode and size
    new_image = PIL.Image.new(mode, size)

    # Add metadata to the image if provided
    if metadata:
        png_info = PIL.PngImagePlugin.PngInfo()
        for key, value in metadata.items():
            png_info.add_text(key, json.dumps(value))
        new_image.info = png_info

    return new_image
