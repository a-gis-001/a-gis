"""Draw the clock hands."""

def _draw_hands(
    *,
    ax: "matplotlib.axes.Axes",
    hour_angle: float,
    minute_angle: float,
    seconds_angle: float,
    hour_hand: "A_GIS.Visual.Clock._Hand",
    minute_hand: "A_GIS.Visual.Clock._Hand",
    second_hand: "A_GIS.Visual.Clock._Hand",
    center: "A_GIS.Visual.Clock._Center",
) -> None:
    """Draw the clock hands.

    Args:
        ax: The axes to draw on.
        hour_angle: Angle for hour hand in radians.
        minute_angle: Angle for minute hand in radians.
        seconds_angle: Angle for second hand in radians.
        hour_hand: Hour hand parameters from _Hand class.
        minute_hand: Minute hand parameters from _Hand class.
        second_hand: Second hand parameters from _Hand class.
        center: Center parameters from _Center class.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Draw hands
    ax.plot(
        [0, hour_hand.length * np.cos(hour_angle)],
        [0, hour_hand.length * np.sin(hour_angle)],
        lw=hour_hand.width,
        color=hour_hand.color,
    )
    ax.plot(
        [0, minute_hand.length * np.cos(minute_angle)],
        [0, minute_hand.length * np.sin(minute_angle)],
        lw=minute_hand.width,
        color=minute_hand.color,
    )
    ax.plot(
        [0, second_hand.length * np.cos(seconds_angle)],
        [0, second_hand.length * np.sin(seconds_angle)],
        lw=second_hand.width,
        color=second_hand.color,
    )

    # Center circle
    ax.add_patch(plt.Circle((0, 0), center.size, color=center.color))
