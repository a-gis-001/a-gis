def test_save_to_array():
    """Test the _save_to_array function."""
    import A_GIS.Visual.Clock._save_to_array
    import matplotlib.pyplot
    import numpy
    import pytest
    
    # Create a simple figure
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    matplotlib.pyplot.axis("off")
    
    # Draw a circle on the figure
    circle = matplotlib.pyplot.Circle((0.5, 0.5), 0.4, color="red")
    ax.add_patch(circle)
    
    # Save the figure to an array
    img_array = A_GIS.Visual.Clock._save_to_array._save_to_array(fig=fig)
    
    # Verify that the result is a numpy array with expected properties
    assert isinstance(img_array, numpy.ndarray)
    assert img_array.ndim == 3  # RGB image with color channels
    assert img_array.shape[2] == 4  # RGBA channels
    
    # Verify that the image contains the red circle
    # (at least some pixels should be red)
    red_pixels = numpy.sum((img_array[:, :, 0] > 200) & 
                          (img_array[:, :, 1] < 50) & 
                          (img_array[:, :, 2] < 50))
    assert red_pixels > 0 