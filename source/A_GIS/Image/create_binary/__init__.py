def create_binary(*, image, threshold=150):
    """Create a binary version of the image."""
    import numpy
    import cv2
    import A_GIS.Code.make_struct
    import PIL

    grayscale = image.convert("L")

    data = numpy.array(grayscale)

    # Thresholding to create a binary image
    _, binary = cv2.threshold(data, threshold, 255, cv2.THRESH_BINARY_INV)

    return A_GIS.Code.make_struct(
        image=PIL.Image.fromarray(binary),
        grayscale=grayscale,
        _threshold=threshold,
        _image=image,
    )
