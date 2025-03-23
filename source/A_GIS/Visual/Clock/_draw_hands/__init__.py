def _draw_hands(*, ax: 'matplotlib.axes.Axes', hour_angle: float, minute_angle: float, seconds_angle: float, 
               hour_color: str = "black", hour_width: float = 6, hour_length: float = 0.5,
               minute_color: str = "black", minute_width: float = 3, minute_length: float = 0.8,
               second_color: str = "red", second_width: float = 1, second_length: float = 0.9,
               center_color: str = "black", center_size: float = 0.02) -> None:
    """Draw the clock hands with customization options.
    
    Args:
        ax (matplotlib.axes.Axes): The axes to draw on.
        hour_angle (float): Angle for hour hand in radians.
        minute_angle (float): Angle for minute hand in radians.
        seconds_angle (float): Angle for seconds hand in radians.
        hour_color (str): Color of the hour hand.
        hour_width (float): Width of the hour hand.
        hour_length (float): Length of the hour hand (0-1 scale).
        minute_color (str): Color of the minute hand.
        minute_width (float): Width of the minute hand.
        minute_length (float): Length of the minute hand (0-1 scale).
        second_color (str): Color of the second hand.
        second_width (float): Width of the second hand.
        second_length (float): Length of the second hand (0-1 scale).
        center_color (str): Color of the center circle.
        center_size (float): Size of the center circle.
    
    Returns:
        None
    """
    import matplotlib.pyplot
    import numpy

    # Draw hour hand
    ax.plot(
        [0, hour_length * numpy.cos(hour_angle)],
        [0, hour_length * numpy.sin(hour_angle)],
        lw=hour_width,
        color=hour_color,
    )
    
    # Draw minute hand
    ax.plot(
        [0, minute_length * numpy.cos(minute_angle)],
        [0, minute_length * numpy.sin(minute_angle)],
        lw=minute_width,
        color=minute_color,
    )
    
    # Draw seconds hand
    ax.plot(
        [0, second_length * numpy.cos(seconds_angle)],
        [0, second_length * numpy.sin(seconds_angle)],
        lw=second_width,
        color=second_color,
    )

    # Center circle
    ax.add_patch(matplotlib.pyplot.Circle((0, 0), center_size, color=center_color)) 