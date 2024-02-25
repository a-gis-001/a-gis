import PIL.Image
import typing


def modify(
    *, image: PIL.Image.Image, metadata: typing.Optional[typing.Dict[str, str]] = None
) -> PIL.Image.Image:
    """
    Modify the metadata of an in-memory image object.

    This function updates the metadata of a given PIL.Image.Image object.
    The metadata is provided as a dictionary, with each key-value pair representing
    a metadata field and its value. The metadata values are serialized to JSON format
    before being added to the image.

    Args:
        image (PIL.Image.Image): The image object whose metadata is to be modified.
        metadata (typing.Optional[typing.Dict[str, str]]): A dictionary containing
            the metadata to be added or modified. Each value is serialized to JSON.
            Defaults to None.

    Returns:
        PIL.Image.Image: The modified image object with updated metadata.

    Examples:
        >>> import A_GIS.Image
        >>> image = A_GIS.Image.new(size=(100,100),metadata={'author1':'me'})
        >>> metadata = A_GIS.Image.Metadata.get(image=image)
        >>> metadata['author1']
            'me'
        >>> image = A_GIS.Image.Metadata.modify(image=image,metadata={'author2':'you')
        >>> metadata = A_GIS.Image.Metadata.get(image=image)
        >>> metadata['author1']
            'me'
        >>> metadata['author2']
            'you'

    Raises:
        ValueError: If the provided metadata is not a dictionary.
    """
    import json
    import PIL.PngImagePlugin

    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary.")

    # Create a new PngInfo object for adding metadata
    png_info = PIL.PngImagePlugin.PngInfo()
    for key, value in (metadata or {}).items():
        # Serialize the metadata value to JSON
        serialized_value = json.dumps(value)
        png_info.add_text(key, serialized_value)

    # Update the image's metadata
    image.info = png_info

    return image
