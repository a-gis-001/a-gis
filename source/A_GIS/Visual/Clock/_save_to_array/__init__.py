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
    import cairosvg

    # Set figure size to 6x6 inches and DPI to 160 to get 960x960 pixels
    fig.set_size_inches(6, 6)
    
    # First save as SVG
    svg_buf = io.BytesIO()
    fig.savefig(svg_buf, format="svg", dpi=160, pad_inches=0, bbox_inches=None)
    svg_buf.seek(0)
    
    # Convert SVG to PNG using cairosvg
    png_buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg_buf.getvalue(), write_to=png_buf, scale=2.0)
    png_buf.seek(0)
    
    # Convert to numpy array
    img = PIL.Image.open(png_buf)
    return numpy.array(img)
