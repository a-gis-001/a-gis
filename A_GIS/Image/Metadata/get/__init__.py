import PIL.Image
import typing


def get(*, image: PIL.Image.Image) -> typing.Dict[str, str]:
    """
    Retrieve the metadata of an in-memory image object as a dictionary.

    This function extracts the metadata from a given PIL.Image.Image object.
    The metadata is stored as JSON-serialized strings within the image object.
    This function deserializes these strings back into their original dictionary format.

    Args:
        image (PIL.Image.Image): The image object from which to retrieve metadata.

    Returns:
        typing.Dict[str, str]: A dictionary containing the deserialized metadata
        of the image. Each key-value pair represents a metadata field and its value.

    Examples:
        >>> import A_GIS.Image
        >>> image = A_GIS.Image.new(size=(100,100), metadata={'author':'me'})
        >>> metadata = A_GIS.Image.Metadata.get(image=image)
        >>> metadata['author']
        'me'

    Raises:
        ValueError: If the image's metadata is not in the expected format.
    """
    import json
    import sys

    metadata = {}
    if hasattr(image, "info"):
        for key, value in image.info.items():
            try:
                # Deserialize the metadata value from JSON
                metadata[key] = json.loads(value)
            except json.JSONDecodeError:
                raise ValueError(
                    f"Metadata for key '{key}' is not in valid JSON format."
                )

    return metadata
