def _calculate_hand_angles(
    *, hour: int, minute: int, second: int
) -> tuple[float, float, float]:
    """Calculate the angles for hour, minute, and seconds hands.

    Args:
        hour (int): Hour value (0-23)
        minute (int): Minute value (0-59)
        second (int): Second value (0-59)

    Returns:
        tuple[float, float, float]: (hour_angle, minute_angle, seconds_angle) in radians
                                   Angles follow standard mathematical convention:
                                   - 12 o'clock = π/2
                                   - 3 o'clock = 0
                                   - 6 o'clock = -π/2
                                   - 9 o'clock = -π
    """
    import numpy

    # Convert 24-hour format to 12-hour format
    hour = hour % 12

    # Calculate angles with 3 o'clock as 0 and clockwise as negative
    # Hour: 30° per hour (π/6) + 0.5° per minute (π/360) + 1/120° per second
    # (π/21600)
    hour_angle = numpy.pi / 2 - (
        hour * numpy.pi / 6
        + minute * numpy.pi / 360
        + second * numpy.pi / 21600
    )

    # Minute: 6° per minute (π/30) + 0.1° per second (π/1800)
    minute_angle = numpy.pi / 2 - (
        minute * numpy.pi / 30 + second * numpy.pi / 1800
    )

    # Second: 6° per second (π/30)
    seconds_angle = numpy.pi / 2 - (second * numpy.pi / 30)

    return hour_angle, minute_angle, seconds_angle
