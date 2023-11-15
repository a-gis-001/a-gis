
def purify(*,image):
    """Purify an image for use in AEGIS.
    
    This should remove all metadata and superfluous information,
    except the actual image data. A purified image will always
    return the same content hash.
    """

    # Create new empty image, same size and mode
    pure_image = type(image).new(mode=image.mode, size=image.size)

    # Copy pixels, but not metadata, across
    pure_image.putdata(image.getdata())

    # Copy palette across, if any
    if 'P' in image.mode: image.putpalette(image.getpalette())
    
    return pure_image

