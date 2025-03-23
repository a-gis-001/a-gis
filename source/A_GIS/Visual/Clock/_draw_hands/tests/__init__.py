import pytest
import matplotlib.pyplot
import numpy
import io
import PIL.Image
import A_GIS.Visual.Clock._draw_hands
import A_GIS.Image

def test_draw_hands():
    """Test the _draw_hands function with various angles and customizations."""
    # Create a figure and axis
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 6))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    
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
    
    # Get the drawn lines
    lines = ax.lines
    patches = ax.patches
    
    # Verify number of elements
    assert len(lines) == 3, "Should have 3 lines (hour, minute, second hands)"
    assert len(patches) == 1, "Should have 1 patch (center circle)"
    
    # Verify hour hand properties
    hour_line = lines[0]
    assert numpy.allclose(hour_line.get_xdata(), [0, 0]), "Hour hand should point straight up"
    assert numpy.allclose(hour_line.get_ydata(), [0, 0.5]), "Hour hand should point straight up"
    assert hour_line.get_color() == "blue", "Hour hand should be blue"
    assert hour_line.get_linewidth() == 4, "Hour hand should have width 4"
    
    # Verify minute hand properties
    minute_line = lines[1]
    assert numpy.allclose(minute_line.get_xdata(), [0, 0]), "Minute hand should point straight up"
    assert numpy.allclose(minute_line.get_ydata(), [0, 0.7]), "Minute hand should point straight up"
    assert minute_line.get_color() == "green", "Minute hand should be green"
    assert minute_line.get_linewidth() == 3, "Minute hand should have width 3"
    
    # Verify second hand properties
    second_line = lines[2]
    assert numpy.allclose(second_line.get_xdata(), [0, 0]), "Second hand should point straight up"
    assert numpy.allclose(second_line.get_ydata(), [0, 0.9]), "Second hand should point straight up"
    assert second_line.get_color() == "red", "Second hand should be red"
    assert second_line.get_linewidth() == 1, "Second hand should have width 1"
    
    # Verify center circle properties
    center_circle = patches[0]
    assert numpy.allclose(center_circle.get_facecolor()[:3], [0, 0, 0]), "Center circle should be black"
    assert center_circle.get_radius() == 0.02, "Center circle should have radius 0.02"
    
    # Clear the axes for next test
    ax.clear()
    
    # Test case 2: 3:00:00 (hands at 90 degrees)
    A_GIS.Visual.Clock._draw_hands(
        ax=ax,
        hour_angle=0,  # 3 o'clock
        minute_angle=0,
        seconds_angle=0,
        hour_length=0.5,
        minute_length=0.7,
        second_length=0.9
    )
    
    # Verify hour hand position
    hour_line = ax.lines[0]
    assert numpy.allclose(hour_line.get_xdata(), [0, 0.5]), "Hour hand should point right"
    assert numpy.allclose(hour_line.get_ydata(), [0, 0]), "Hour hand should point right"
    
    # Verify minute hand position
    minute_line = ax.lines[1]
    assert numpy.allclose(minute_line.get_xdata(), [0, 0.7]), "Minute hand should point right"
    assert numpy.allclose(minute_line.get_ydata(), [0, 0]), "Minute hand should point right"
    
    # Verify second hand position
    second_line = ax.lines[2]
    assert numpy.allclose(second_line.get_xdata(), [0, 0.9]), "Second hand should point right"
    assert numpy.allclose(second_line.get_ydata(), [0, 0]), "Second hand should point right"
    
    matplotlib.pyplot.close() 