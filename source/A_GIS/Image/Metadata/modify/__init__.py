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
        >>> image = A_GIS.Image.Metadata.modify(image=image,metadata={'author2':'you'})
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
    import A_GIS.File.Directory
    import pathlib

    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary.")

    pnginfo = PIL.PngImagePlugin.PngInfo()
    # Copy existing meta data.
    for key, value in image.info.items():
        pnginfo.add_text(key, value)
    # Write/overwrite with new metadata.
    for key, value in metadata.items():
        pnginfo.add_text(key, json.dumps(value))
    tempdir = A_GIS.File.Directory.make(scoped_delete=True)
    path = pathlib.Path(tempdir.path) / "new.png"
    image.save(path, "PNG", pnginfo=pnginfo)
    return PIL.Image.open(path)
