import pytest
import matplotlib.pyplot
import numpy
import A_GIS.Visual.Clock._draw_hands
import A_GIS.Image
import os

def save_clock_image(ax, filename):
    """Helper function to save the current clock image."""
    # Ensure the test directory exists
    test_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(test_dir, filename)
    
    # Save the figure
    matplotlib.pyplot.savefig(output_path, dpi=100, bbox_inches='tight')
    matplotlib.pyplot.close()

def setup_axes():
    """Helper function to set up matplotlib axes for testing."""
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    return fig, ax

def verify_hand_properties(line, expected_x, expected_y, color, width, length):
    """Helper function to verify hand properties."""
    assert numpy.allclose(line.get_xdata(), [0, expected_x]), f"Hand should point to ({expected_x}, {expected_y})"
    assert numpy.allclose(line.get_ydata(), [0, expected_y]), f"Hand should point to ({expected_x}, {expected_y})"
    assert line.get_color() == color, f"Hand should be {color}"
    assert line.get_linewidth() == width, f"Hand should have width {width}"

def test_draw_hands_basic():
    """Test the _draw_hands function with basic 12:00:00 position."""
    fig, ax = setup_axes()
    
    # Test case 1: 12:00:00 (all hands pointing up)
    A_GIS.Visual.Clock._draw_hands(
        ax=ax,
        hour_angle=numpy.pi/2,
        minute_angle=numpy.pi/2,
        seconds_angle=numpy.pi/2,
        hour_color="blue",
        minute_color="green",
        second_color="red",
        hour_width=4,
        minute_width=3,
        second_width=1,
        hour_length=0.5,
        minute_length=0.7,
        second_length=0.9,
        center_color="black",
        center_size=0.02
    )
    
    # Get the drawn elements
    lines = ax.lines
    patches = ax.patches
    
    # Verify number of elements
    assert len(lines) == 3, "Should have 3 lines (hour, minute, second hands)"
    assert len(patches) == 1, "Should have 1 patch (center circle)"
    
    # Verify hands
    verify_hand_properties(lines[0], 0, 0.5, "blue", 4, 0.5)  # Hour hand
    verify_hand_properties(lines[1], 0, 0.7, "green", 3, 0.7)  # Minute hand
    verify_hand_properties(lines[2], 0, 0.9, "red", 1, 0.9)  # Second hand
    
    # Verify center circle
    center_circle = patches[0]
    assert numpy.allclose(center_circle.get_facecolor()[:3], [0, 0, 0]), "Center circle should be black"
    assert center_circle.get_radius() == 0.02, "Center circle should have radius 0.02"
    
    # Save the image
    save_clock_image(ax, "clock_12_00_00.png")

def test_draw_hands_positions():
    """Test the _draw_hands function with various clock positions."""
    positions = [
        (0, "3:00", 0.5, 0),  # 3 o'clock
        (numpy.pi, "9:00", -0.5, 0),  # 9 o'clock
        (numpy.pi/2, "12:00", 0, 0.5),  # 12 o'clock
        (-numpy.pi/2, "6:00", 0, -0.5),  # 6 o'clock
        (numpy.pi/4, "1:30", numpy.cos(numpy.pi/4) * 0.5, numpy.sin(numpy.pi/4) * 0.5),  # 1:30
        (-numpy.pi/4, "10:30", numpy.cos(-numpy.pi/4) * 0.5, numpy.sin(-numpy.pi/4) * 0.5),  # 10:30
    ]
    
    for angle, position, expected_x, expected_y in positions:
        fig, ax = setup_axes()
        
        A_GIS.Visual.Clock._draw_hands(
            ax=ax,
            hour_angle=angle,
            minute_angle=angle,
            seconds_angle=angle,
            hour_length=0.5,
            minute_length=0.7,
            second_length=0.9
        )
        
        # Verify hour hand position
        hour_line = ax.lines[0]
        verify_hand_properties(hour_line, expected_x, expected_y, "black", 6, 0.5)
        
        # Save the image
        filename = f"clock_{position.replace(':', '_')}.png"
        save_clock_image(ax, filename)
        matplotlib.pyplot.close()

def test_draw_hands_edge_cases():
    """Test the _draw_hands function with edge cases."""
    # Test negative angles
    fig, ax = setup_axes()
    A_GIS.Visual.Clock._draw_hands(
        ax=ax,
        hour_angle=-numpy.pi/2,
        minute_angle=-numpy.pi/2,
        seconds_angle=-numpy.pi/2,
        hour_length=0.5,
        minute_length=0.7,
        second_length=0.9
    )
    
    # Verify hands point down (6:00 position)
    verify_hand_properties(ax.lines[0], 0, -0.5, "black", 6, 0.5)
    verify_hand_properties(ax.lines[1], 0, -0.7, "black", 3, 0.7)
    verify_hand_properties(ax.lines[2], 0, -0.9, "red", 1, 0.9)
    
    # Save the image
    save_clock_image(ax, "clock_negative_angles.png")

def test_draw_hands_aspect_ratio():
    """Test the _draw_hands function with different aspect ratios."""
    # Test with non-square aspect ratio
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 4))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('auto')
    
    A_GIS.Visual.Clock._draw_hands(
        ax=ax,
        hour_angle=numpy.pi/2,
        minute_angle=numpy.pi/2,
        seconds_angle=numpy.pi/2,
        hour_length=0.5,
        minute_length=0.7,
        second_length=0.9
    )
    
    # Verify hands still point up despite different aspect ratio
    verify_hand_properties(ax.lines[0], 0, 0.5, "black", 6, 0.5)
    verify_hand_properties(ax.lines[1], 0, 0.7, "black", 3, 0.7)
    verify_hand_properties(ax.lines[2], 0, 0.9, "red", 1, 0.9)
    
    # Save the image
    save_clock_image(ax, "clock_aspect_ratio.png")

def test_draw_hands_hand_overlap():
    """Test the _draw_hands function with overlapping hands."""
    fig, ax = setup_axes()
    
    # Test with all hands at same position (12:00:00)
    A_GIS.Visual.Clock._draw_hands(
        ax=ax,
        hour_angle=numpy.pi/2,
        minute_angle=numpy.pi/2,
        seconds_angle=numpy.pi/2,
        hour_length=0.5,
        minute_length=0.7,
        second_length=0.9
    )
    
    # Verify hands are drawn in correct order (second on top)
    assert ax.lines[2].get_zorder() > ax.lines[1].get_zorder(), "Second hand should be on top"
    assert ax.lines[1].get_zorder() > ax.lines[0].get_zorder(), "Minute hand should be above hour hand"
    
    # Save the image
    save_clock_image(ax, "clock_hand_overlap.png")

def test_draw_hands_invalid_inputs():
    """Test the _draw_hands function with invalid inputs."""
    fig, ax = setup_axes()
    
    # Test with invalid colors
    with pytest.raises(ValueError):
        A_GIS.Visual.Clock._draw_hands(
            ax=ax,
            hour_angle=0,
            minute_angle=0,
            seconds_angle=0,
            hour_color="invalid_color"
        )
    
    # Test with negative lengths
    with pytest.raises(ValueError):
        A_GIS.Visual.Clock._draw_hands(
            ax=ax,
            hour_angle=0,
            minute_angle=0,
            seconds_angle=0,
            hour_length=-0.5
        )
    
    # Test with negative widths
    with pytest.raises(ValueError):
        A_GIS.Visual.Clock._draw_hands(
            ax=ax,
            hour_angle=0,
            minute_angle=0,
            seconds_angle=0,
            hour_width=-1
        )
    
    matplotlib.pyplot.close() 