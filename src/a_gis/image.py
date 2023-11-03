def image(existing):
    """Canonicalize an image for use in AEGIS."""

    from PIL import Image

    # Create new empty image, same size and mode
    stripped = Image.new(existing.mode, existing.size)

    # Copy pixels, but not metadata, across
    stripped.putdata(existing.getdata())

    # Copy palette across, if any
    if 'P' in existing.mode: stripped.putpalette(existing.getpalette())
    
    return stripped

