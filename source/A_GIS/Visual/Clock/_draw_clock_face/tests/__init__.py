def test_draw_clock_face():
    """Test the _draw_clock_face function."""
    import A_GIS.Visual.Clock._draw_clock_face
    import A_GIS.Image
    import matplotlib.pyplot
    import numpy
    import PIL.Image
    import io
    import os
    
    # Create output directory if it doesn't exist
    test_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(test_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a reference clock face image with default parameters
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.2)  # Add some padding
    ax.set_ylim(-1.2, 1.2)  # Add some padding
    matplotlib.pyplot.axis('off')
    
    # Draw the outer circle
    circle = matplotlib.pyplot.Circle((0, 0), 1.0, facecolor='white', edgecolor='black', linewidth=3)
    ax.add_patch(circle)
    
    # Draw hour markers
    for hour in range(12):
        angle = numpy.pi/2 - (hour * numpy.pi/6)  # Start from 12 o'clock
        marker_length = 0.1  # Length of hour markers
        
        # Calculate marker start and end points
        outer_r = 1.0
        inner_r = outer_r - marker_length
        
        x1 = outer_r * numpy.cos(angle)
        y1 = outer_r * numpy.sin(angle)
        x2 = inner_r * numpy.cos(angle)
        y2 = inner_r * numpy.sin(angle)
        
        # Draw the hour marker
        ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)
    
    # Save reference image
    reference_path = os.path.join(output_dir, "clock_face_reference.png")
    matplotlib.pyplot.savefig(reference_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
    
    # Load reference image for comparison
    reference_image = PIL.Image.open(reference_path)
    
    # Generate test image using _draw_clock_face with defaults
    test_fig, test_ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    test_ax.set_aspect('equal')
    test_ax.set_xlim(-1.2, 1.2)  # Add some padding
    test_ax.set_ylim(-1.2, 1.2)  # Add some padding
    matplotlib.pyplot.axis('off')
    
    A_GIS.Visual.Clock._draw_clock_face(ax=test_ax)
    
    # Save test image
    test_path = os.path.join(output_dir, "clock_face_test.png")
    matplotlib.pyplot.savefig(test_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close(test_fig)
    
    # Load test image for comparison
    test_image = PIL.Image.open(test_path)
    
    # Compare images
    result = A_GIS.Image.compare(
        image1=reference_image,
        image2=test_image,
        tolerance=0.95
    )
    
    # The images should be very similar
    assert result.ssim > 0.95, f"Clock face does not match reference image (SSIM: {result.ssim})"
    assert result.are_similar == True, "Clock face does not match reference image"
    
    # Test with all features enabled
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)  # Add some padding
    ax.set_ylim(-1.2, 1.2)  # Add some padding
    matplotlib.pyplot.axis("off")
    
    A_GIS.Visual.Clock._draw_clock_face(
        ax=ax,
        face=A_GIS.Visual.Clock.init_face(
            color='white',
            edge_color='red',
            edge_width=3,
            tick_color='red',
            tick_width=2,
            hour_marker_length=0.1,
            minute_marker_factor=0.5,
            number_mode='all',
            number_size=0.1,
            number_font='Arial'
        )
    )
    
    # Save all-features test image
    all_features_path = os.path.join(output_dir, "clock_face_all_features.png")
    matplotlib.pyplot.savefig(all_features_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
    
    # Test with four numbers only
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)  # Add some padding
    ax.set_ylim(-1.2, 1.2)  # Add some padding
    matplotlib.pyplot.axis("off")
    
    A_GIS.Visual.Clock._draw_clock_face(
        ax=ax,
        face=A_GIS.Visual.Clock.init_face(
            color='white',
            edge_color='blue',
            edge_width=3,
            tick_color='blue',
            tick_width=2,
            hour_marker_length=0.1,
            minute_marker_factor=0.5,
            number_mode='four',
            number_size=0.1,
            number_font='Arial'
        )
    )
    
    # Save four-numbers test image
    four_numbers_path = os.path.join(output_dir, "clock_face_four_numbers.png")
    matplotlib.pyplot.savefig(four_numbers_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
    
    # Test with minute markers only
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)  # Add some padding
    ax.set_ylim(-1.2, 1.2)  # Add some padding
    matplotlib.pyplot.axis("off")
    
    A_GIS.Visual.Clock._draw_clock_face(
        ax=ax,
        face=A_GIS.Visual.Clock.init_face(
            color='white',
            edge_color='green',
            edge_width=3,
            tick_color='green',
            tick_width=2,
            hour_marker_length=0.1,
            minute_marker_factor=0.5,
            number_mode='none',
            number_size=0.1,
            number_font='Arial'
        )
    )
    
    # Save minute-markers test image
    minute_markers_path = os.path.join(output_dir, "clock_face_minute_markers.png")
    matplotlib.pyplot.savefig(minute_markers_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close(fig)
    
    # Verify that the clock face and ticks were drawn
    assert len(ax.patches) == 1  # Clock face
    assert len(ax.lines) == 72   # Hour ticks (12) + minute ticks (60)
    
    # Verify the clock face properties
    clock_face = ax.patches[0]
    assert clock_face.get_edgecolor()[0:3] == matplotlib.colors.to_rgb("green")
    assert clock_face.get_linewidth() == 3
    
    # Verify tick properties
    for line in ax.lines:
        assert line.get_color() == "green"
        assert line.get_linewidth() == 2 