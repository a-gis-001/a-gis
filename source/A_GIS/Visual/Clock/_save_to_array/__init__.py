def _save_to_array(*, fig: "matplotlib.figure.Figure") -> "numpy.ndarray":
    """Save figure to numpy array.

    Args:
        fig (matplotlib.figure.Figure): The figure to save

    Returns:
        numpy.ndarray: The image as a numpy array
    """
    import io
    import PIL.Image
    import numpy

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = PIL.Image.open(buf)
    return numpy.array(img)
