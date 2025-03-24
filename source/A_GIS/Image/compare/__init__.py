def compare(
    *,
    image1: "type['PIL.Image.Image'] | type['numpy.ndarray']",
    image2: "type['PIL.Image.Image'] | type['numpy.ndarray']",
    tolerance: float = 0.95,
) -> "type['A_GIS.Code.make_struct']":
    """Compare two images and return similarity metrics.

    This function compares two images using multiple metrics:
    1. Mean Squared Error (MSE) - lower is better
    2. Structural Similarity Index (SSIM) - higher is better (max 1.0)

    Args:
        image1: First image to compare (PIL.Image or numpy array)
        image2: Second image to compare (PIL.Image or numpy array)
        tolerance: SSIM threshold for considering images similar enough (default 0.95)

    Returns:
        A_GIS.Code.make_struct with fields:
            - mse: Mean Squared Error between images
            - ssim: Structural Similarity Index
            - are_similar: Boolean indicating if SSIM >= tolerance
            - error: Error message if validation fails, empty string otherwise
            - _image1: First input image
            - _image2: Second input image
            - _tolerance: Input tolerance value

    Examples:
        >>> import A_GIS.Image.compare
        >>> import A_GIS.Image.new
        >>> # Create two identical images
        >>> img1 = A_GIS.Image.new(size=(100, 100), mode='RGB', color=(255, 0, 0))
        >>> img2 = A_GIS.Image.new(size=(100, 100), mode='RGB', color=(255, 0, 0))
        >>> result = A_GIS.Image.compare(image1=img1, image2=img2)
        >>> result.are_similar
        True
    """
    import numpy
    import PIL.Image
    import skimage
    import A_GIS.Code.make_struct

    error = ""
    if not isinstance(
        image1, (PIL.Image.Image, numpy.ndarray)
    ) or not isinstance(image2, (PIL.Image.Image, numpy.ndarray)):
        error = "Images must be PIL.Image or numpy array"
        return A_GIS.Code.make_struct(
            mse=0.0,
            ssim=0.0,
            are_similar=False,
            error=error,
            _image1=image1,
            _image2=image2,
            _tolerance=tolerance,
        )

    if not 0 <= tolerance <= 1:
        error = "Tolerance must be between 0 and 1"
        return A_GIS.Code.make_struct(
            mse=0.0,
            ssim=0.0,
            are_similar=False,
            error=error,
            _image1=image1,
            _image2=image2,
            _tolerance=tolerance,
        )

    # Convert PIL Images to numpy arrays if needed
    if isinstance(image1, PIL.Image.Image):
        image1 = numpy.array(image1)
    if isinstance(image2, PIL.Image.Image):
        image2 = numpy.array(image2)

    # Ensure images have same dimensions and channels
    if image1.shape != image2.shape:
        error = f"Images must have same dimensions. Got {
            image1.shape} vs {
            image2.shape}"
        return A_GIS.Code.make_struct(
            mse=0.0,
            ssim=0.0,
            are_similar=False,
            error=error,
            _image1=image1,
            _image2=image2,
            _tolerance=tolerance,
        )

    # Handle special cases for small images
    if 0 in image1.shape or 0 in image2.shape:  # Empty images
        return A_GIS.Code.make_struct(
            mse=0.0,
            ssim=1.0,
            are_similar=True,
            error=error,
            _image1=image1,
            _image2=image2,
            _tolerance=tolerance,
        )

    if image1.shape[0] < 7 or image1.shape[1] < 7:  # Images smaller than 7x7
        # For small images, only use MSE and a stricter threshold
        mse = numpy.mean((image1 - image2) ** 2)
        are_similar = mse < 1.0  # Very small threshold for small images
        return A_GIS.Code.make_struct(
            mse=float(mse),
            ssim=(
                1.0 if are_similar else 0.0
            ),  # Use binary SSIM for small images
            are_similar=are_similar,
            error=error,
            _image1=image1,
            _image2=image2,
            _tolerance=tolerance,
        )

    # Calculate MSE
    mse = numpy.mean((image1.astype(float) - image2.astype(float)) ** 2)

    # Calculate SSIM
    # For RGBA images, we need to handle the alpha channel separately
    if len(image1.shape) == 3:
        if image1.shape[2] == 4:  # RGBA
            # Compare RGB channels
            ssim_rgb = skimage.metrics.structural_similarity(
                image1[..., :3],
                image2[..., :3],
                channel_axis=2,
                win_size=7,  # Use minimum window size
            )
            # Compare alpha channel
            ssim_alpha = skimage.metrics.structural_similarity(
                image1[..., 3], image2[..., 3], win_size=7
            )
            # Combine RGB and alpha similarities
            ssim = (ssim_rgb + ssim_alpha) / 2
        elif image1.shape[2] == 3:  # RGB
            ssim = skimage.metrics.structural_similarity(
                image1, image2, channel_axis=2, win_size=7
            )
        else:  # Other multichannel
            ssim = skimage.metrics.structural_similarity(
                image1, image2, channel_axis=2, win_size=7
            )
    else:  # Grayscale
        ssim = skimage.metrics.structural_similarity(
            image1, image2, win_size=7
        )

    return A_GIS.Code.make_struct(
        mse=float(mse),
        ssim=float(ssim),
        are_similar=ssim >= tolerance,
        error=error,
        _image1=image1,
        _image2=image2,
        _tolerance=tolerance,
    )
