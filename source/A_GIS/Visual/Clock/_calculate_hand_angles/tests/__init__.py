def test_calculate_hand_angles():
    """Test the _calculate_hand_angles function."""
    from A_GIS.Visual.Clock import _calculate_hand_angles
    import math
    import pytest
    
    # Test case 1: 12:00:00 (all hands at 12)
    hour_angle, minute_angle, seconds_angle = _calculate_hand_angles(
        hour=12, minute=0, second=0)
    print(f"\nTest case 1 (12:00:00):")
    print(f"hour_angle: expected={math.pi/2}, got={hour_angle}")
    print(f"minute_angle: expected={math.pi/2}, got={minute_angle}")
    print(f"seconds_angle: expected={math.pi/2}, got={seconds_angle}")
    assert math.isclose(hour_angle, math.pi/2, abs_tol=1e-10)  # 12 o'clock = π/2
    assert math.isclose(minute_angle, math.pi/2, abs_tol=1e-10)  # 0 minutes = π/2
    assert math.isclose(seconds_angle, math.pi/2, abs_tol=1e-10)  # 0 seconds = π/2
    
    # Test case 2: 6:30:15 (hour between 6 and 7, minute at 6, second at 3)
    hour_angle, minute_angle, seconds_angle = _calculate_hand_angles(
        hour=6, minute=30, second=15)
    # Hour: 6:30:15 = -π/2 - (30/60 * π/6) - (15/3600 * π/6)
    expected_hour = -math.pi/2 - (30/60 * math.pi/6) - (15/3600 * math.pi/6)
    # Minute: 30:15 = -π/2 - (15/60 * π/30)
    expected_minute = -math.pi/2 - (15/60 * math.pi/30)
    # Second: 15 = 0 (3 o'clock)
    expected_second = 0
    print(f"\nTest case 2 (6:30:15):")
    print(f"hour_angle: expected={expected_hour}, got={hour_angle}")
    print(f"minute_angle: expected={expected_minute}, got={minute_angle}")
    print(f"seconds_angle: expected={expected_second}, got={seconds_angle}")
    assert math.isclose(hour_angle, expected_hour, abs_tol=1e-10)
    assert math.isclose(minute_angle, expected_minute, abs_tol=1e-10)
    assert math.isclose(seconds_angle, expected_second, abs_tol=1e-10)
    
    # Test case 3: 3:15:30 (hour at 3, minute at 3, second at 6)
    hour_angle, minute_angle, seconds_angle = _calculate_hand_angles(
        hour=3, minute=15, second=30)
    # Hour: 3:15:30 = 0 - (15/60 * π/6) - (30/3600 * π/6)
    expected_hour = 0 - (15/60 * math.pi/6) - (30/3600 * math.pi/6)
    # Minute: 15:30 = 0 - (30/60 * π/30)
    expected_minute = 0 - (30/60 * math.pi/30)
    # Second: 30 = -π/2 (6 o'clock)
    expected_second = -math.pi/2
    print(f"\nTest case 3 (3:15:30):")
    print(f"hour_angle: expected={expected_hour}, got={hour_angle}")
    print(f"minute_angle: expected={expected_minute}, got={minute_angle}")
    print(f"seconds_angle: expected={expected_second}, got={seconds_angle}")
    assert math.isclose(hour_angle, expected_hour, abs_tol=1e-10)
    assert math.isclose(minute_angle, expected_minute, abs_tol=1e-10)
    assert math.isclose(seconds_angle, expected_second, abs_tol=1e-10)
    
    # Test case 4: 9:45:45 (hour at 9, minute at 9, second at 9)
    hour_angle, minute_angle, seconds_angle = _calculate_hand_angles(
        hour=9, minute=45, second=45)
    # Hour: 9:45:45 = -π - (45/60 * π/6) - (45/3600 * π/6)
    expected_hour = -math.pi - (45/60 * math.pi/6) - (45/3600 * math.pi/6)
    # Minute: 45:45 = -π - (45/60 * π/30)
    expected_minute = -math.pi - (45/60 * math.pi/30)
    # Second: 45 = -π (9 o'clock)
    expected_second = -math.pi
    print(f"\nTest case 4 (9:45:45):")
    print(f"hour_angle: expected={expected_hour}, got={hour_angle}")
    print(f"minute_angle: expected={expected_minute}, got={minute_angle}")
    print(f"seconds_angle: expected={expected_second}, got={seconds_angle}")
    assert math.isclose(hour_angle, expected_hour, abs_tol=1e-10)
    assert math.isclose(minute_angle, expected_minute, abs_tol=1e-10)
    assert math.isclose(seconds_angle, expected_second, abs_tol=1e-10)
    
    # Test case 5: 0:00:00 (midnight - all hands at 12)
    hour_angle, minute_angle, seconds_angle = _calculate_hand_angles(
        hour=0, minute=0, second=0)
    print(f"\nTest case 5 (0:00:00):")
    print(f"hour_angle: expected={math.pi/2}, got={hour_angle}")
    print(f"minute_angle: expected={math.pi/2}, got={minute_angle}")
    print(f"seconds_angle: expected={math.pi/2}, got={seconds_angle}")
    assert math.isclose(hour_angle, math.pi/2, abs_tol=1e-10)  # 0/12 hours = π/2 (12 o'clock)
    assert math.isclose(minute_angle, math.pi/2, abs_tol=1e-10)  # 0 minutes = π/2 (12 o'clock)
    assert math.isclose(seconds_angle, math.pi/2, abs_tol=1e-10)  # 0 seconds = π/2 (12 o'clock)
