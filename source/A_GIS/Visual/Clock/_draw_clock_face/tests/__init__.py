def test_draw_clock_face():
    """Test the _draw_clock_face function."""
    import A_GIS.Visual.Clock._draw_clock_face
    import A_GIS.Image
    import matplotlib.pyplot
    import numpy
    import PIL.Image
    import io
    
    # Create a reference clock face image
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    matplotlib.pyplot.axis('off')
    
    # Draw the outer circle
    circle = matplotlib.pyplot.Circle((0.5, 0.5), 0.4, fill=False, color='black')
    ax.add_patch(circle)
    
    # Draw hour markers
    for hour in range(12):
        angle = numpy.pi/2 - (hour * numpy.pi/6)  # Start from 12 o'clock
        marker_length = 0.08  # Length of hour markers
        
        # Calculate marker start and end points
        outer_r = 0.4
        inner_r = outer_r - marker_length
        
        x1 = 0.5 + outer_r * numpy.cos(angle)
        y1 = 0.5 + outer_r * numpy.sin(angle)
        x2 = 0.5 + inner_r * numpy.cos(angle)
        y2 = 0.5 + inner_r * numpy.sin(angle)
        
        # Draw the hour marker
        ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)
    
    # Save reference image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    reference_image = PIL.Image.open(buf)
    matplotlib.pyplot.close(fig)
    
    # Generate test image using _draw_clock_face
    test_fig, test_ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    test_ax.set_aspect('equal')
    matplotlib.pyplot.axis('off')
    
    A_GIS.Visual.Clock._draw_clock_face(ax=test_ax)
    
    # Save test image
    test_buf = io.BytesIO()
    test_fig.savefig(test_buf, format='png', bbox_inches='tight', dpi=100)
    test_buf.seek(0)
    test_image = PIL.Image.open(test_buf)
    matplotlib.pyplot.close(test_fig)
    
    # Compare images
    result = A_GIS.Image.compare(
        image1=reference_image,
        image2=test_image,
        tolerance=0.95
    )
    
    # The images should be very similar
    assert result.ssim > 0.95, f"Clock face does not match reference image (SSIM: {result.ssim})"
    assert result.are_similar == True, "Clock face does not match reference image"
    
    # Test with custom parameters
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    matplotlib.pyplot.axis("off")
    
    A_GIS.Visual.Clock._draw_clock_face(
        ax=ax,
        radius=0.3,
        center=(0.4, 0.6),
        marker_length=0.1,
        color='red',
        linewidth=3
    )
    
    # Verify that the clock face and ticks were drawn
    assert len(ax.patches) == 1  # Clock face
    assert len(ax.lines) == 12   # Hour ticks
    
    # Verify the clock face properties
    clock_face = ax.patches[0]
    assert clock_face.get_edgecolor()[0:3] == matplotlib.colors.to_rgb("red")
    assert clock_face.get_linewidth() == 3
    
    # Verify tick properties
    for line in ax.lines:
        assert line.get_color() == "red"
        assert line.get_linewidth() == 3 