"""Tests for the clock render function."""
import os
import pytest
import numpy
import PIL.Image
import matplotlib.pyplot
import A_GIS.Visual.Clock.render

def test_render_basic_functionality():
    """Test basic clock rendering functionality."""
    result = A_GIS.Visual.Clock.render.render(hour=12, minute=0, second=0)
    assert isinstance(result.image, numpy.ndarray)
    assert result._hour == 12
    assert result._minute == 0
    assert result._second == 0
    assert result.image.shape[2] == 4  # RGBA format

    # Test with customization options
    result = A_GIS.Visual.Clock.render.render(
        hour=12, 
        minute=0, 
        second=0,
        face_color="blue",
        edge_color="red",
        hour_color="green",
        minute_color="purple",
        second_color="orange"
    )
    assert isinstance(result.image, numpy.ndarray)
    assert result._hour == 12
    assert result._minute == 0
    assert result._second == 0

def test_render_hand_positions():
    """Test that clock hands are rendered in correct positions."""
    # Test 12:00:00 - hands should point up
    result_12 = A_GIS.Visual.Clock.render.render(hour=12, minute=0, second=0)
    # Test 3:00:00 - hour hand should point right
    result_3 = A_GIS.Visual.Clock.render.render(hour=3, minute=0, second=0)
    # Test 6:00:00 - hour hand should point down
    result_6 = A_GIS.Visual.Clock.render.render(hour=6, minute=0, second=0)
    # Test 9:00:00 - hour hand should point left
    result_9 = A_GIS.Visual.Clock.render.render(hour=9, minute=0, second=0)
    # Test with different seconds positions
    result_s15 = A_GIS.Visual.Clock.render.render(hour=12, minute=0, second=15)
    result_s30 = A_GIS.Visual.Clock.render.render(hour=12, minute=0, second=30)
    result_s45 = A_GIS.Visual.Clock.render.render(hour=12, minute=0, second=45)

    # Compare images to verify hand positions
    assert not numpy.array_equal(result_12.image, result_3.image)
    assert not numpy.array_equal(result_3.image, result_6.image)
    assert not numpy.array_equal(result_6.image, result_9.image)
    assert not numpy.array_equal(result_12.image, result_s15.image)
    assert not numpy.array_equal(result_s15.image, result_s30.image)
    assert not numpy.array_equal(result_s30.image, result_s45.image)

def test_render_input_validation():
    """Test input validation for the render function."""
    # Test invalid types
    with pytest.raises(TypeError, match="hour must be an integer"):
        A_GIS.Visual.Clock.render.render(hour=12.5, minute=0, second=0)
    with pytest.raises(TypeError, match="minute must be an integer"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=30.5, second=0)
    with pytest.raises(TypeError, match="second must be an integer"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=30, second=30.5)
    
    # Test invalid ranges
    with pytest.raises(ValueError, match="hour must be between 0 and 23"):
        A_GIS.Visual.Clock.render.render(hour=24, minute=0, second=0)
    with pytest.raises(ValueError, match="hour must be between 0 and 23"):
        A_GIS.Visual.Clock.render.render(hour=-1, minute=0, second=0)
    with pytest.raises(ValueError, match="minute must be between 0 and 59"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=60, second=0)
    with pytest.raises(ValueError, match="minute must be between 0 and 59"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=-1, second=0)
    with pytest.raises(ValueError, match="second must be between 0 and 59"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=30, second=60)
    with pytest.raises(ValueError, match="second must be between 0 and 59"):
        A_GIS.Visual.Clock.render.render(hour=12, minute=30, second=-1) 