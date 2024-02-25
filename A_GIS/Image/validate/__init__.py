import PIL.Image


def validate(image: PIL.Image.Image):
    if not hasattr(image, "info") or image.info is None:
        raise ValueError("image must have metadata!")
    pass
