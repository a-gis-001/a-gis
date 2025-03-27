"""Tests for the clock render function."""
import A_GIS.Visual.Clock.render

def test_render_basic_functionality():
    """Test basic clock rendering functionality."""
    result = A_GIS.Visual.Clock.render(hour=12, minute=0, second=0)
    assert result.error == ""
    assert isinstance(result.svg, str)  # Check for SVG code
    assert result._hour == 12
    assert result._minute == 0
    assert result._second == 0

    result = A_GIS.Visual.Clock.render(
        hour=12, 
        minute=0, 
        second=0,
    )
    assert result.error == ""
    assert isinstance(result.svg, str)  # Check for SVG code
    print(result.svg)
    assert result._hour == 12
    assert result._minute == 0
    assert result._second == 0

def test_render_hand_positions():
    """Test that clock hands are rendered in correct positions."""
    # Test 12:00:00 - hands should point up
    result_12 = A_GIS.Visual.Clock.render(hour=12, minute=0, second=0)
    # Test 3:00:00 - hour hand should point right
    result_3 = A_GIS.Visual.Clock.render(hour=3, minute=0, second=0)
    # Test 6:00:00 - hour hand should point down
    result_6 = A_GIS.Visual.Clock.render(hour=6, minute=0, second=0)
    # Test 9:00:00 - hour hand should point left
    result_9 = A_GIS.Visual.Clock.render(hour=9, minute=0, second=0)
    # Test with different seconds positions
    result_s15 = A_GIS.Visual.Clock.render(hour=12, minute=0, second=15)
    result_s30 = A_GIS.Visual.Clock.render(hour=12, minute=0, second=30)
    result_s45 = A_GIS.Visual.Clock.render(hour=12, minute=0, second=45)

    # Verify no errors
    assert result_12.error == ""
    assert result_3.error == ""
    assert result_6.error == ""
    assert result_9.error == ""
    assert result_s15.error == ""
    assert result_s30.error == ""
    assert result_s45.error == ""

    # Compare SVG codes to verify hand positions
    assert result_12.svg != result_3.svg
    assert result_3.svg != result_6.svg
    assert result_6.svg != result_9.svg
    assert result_12.svg != result_s15.svg
    assert result_s15.svg != result_s30.svg
    assert result_s30.svg != result_s45.svg

def test_render_input_validation():
    """Test input validation for the render function."""
    # Test invalid types
    result = A_GIS.Visual.Clock.render(hour=12.5, minute=0, second=0)
    assert result.error == "hour must be an integer"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=30.5, second=0)
    assert result.error == "minute must be an integer"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=30, second=30.5)
    assert result.error == "second must be an integer"
    assert result.svg is None
    
    # Test invalid ranges
    result = A_GIS.Visual.Clock.render(hour=24, minute=0, second=0)
    assert result.error == "hour must be between 0 and 23"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=-1, minute=0, second=0)
    assert result.error == "hour must be between 0 and 23"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=60, second=0)
    assert result.error == "minute must be between 0 and 59"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=-1, second=0)
    assert result.error == "minute must be between 0 and 59"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=30, second=60)
    assert result.error == "second must be between 0 and 59"
    assert result.svg is None

    result = A_GIS.Visual.Clock.render(hour=12, minute=30, second=-1)
    assert result.error == "second must be between 0 and 59"
    assert result.svg is None 