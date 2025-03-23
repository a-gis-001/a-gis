def _draw_clock_face(ax):
    """Draw the clock face and hour ticks.

    Args:
        ax (matplotlib.axes.Axes): The axes to draw on.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Draw clock face
    clock_face = plt.Circle((0, 0), 1, color="white", ec="black", lw=3)
    ax.add_patch(clock_face)

    # Draw hour ticks
    for i in range(12):
        angle = np.pi / 6 * i
        ax.plot(
            [0.9 * np.cos(angle), np.cos(angle)],
            [0.9 * np.sin(angle), np.sin(angle)],
            color="black",
            lw=2,
        )

def _calculate_hand_angles(hour, minute):
    """Calculate the angles for hour and minute hands.

    Args:
        hour (int): Hour value (0-23)
        minute (int): Minute value (0-59)

    Returns:
        tuple: (hour_angle, minute_angle) in radians
    """
    import numpy as np

    # Convert 24-hour format to 12-hour format
    hour = hour % 12
    if hour == 0:
        hour = 12

    hour_angle = np.pi / 2 - (np.pi / 6 * (hour % 12 + minute / 60))
    minute_angle = np.pi / 2 - (np.pi / 30 * minute)

    return hour_angle, minute_angle

def _draw_hands(ax, hour_angle, minute_angle):
    """Draw the hour and minute hands.

    Args:
        ax (matplotlib.axes.Axes): The axes to draw on
        hour_angle (float): Angle for hour hand in radians
        minute_angle (float): Angle for minute hand in radians
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Draw hands
    ax.plot(
        [0, 0.5 * np.cos(hour_angle)],
        [0, 0.5 * np.sin(hour_angle)],
        lw=6,
        color="black",
    )
    ax.plot(
        [0, 0.8 * np.cos(minute_angle)],
        [0, 0.8 * np.sin(minute_angle)],
        lw=3,
        color="black",
    )

    # Center circle
    ax.add_patch(plt.Circle((0, 0), 0.02, color="black"))

def _create_figure():
    """Create a new figure with equal aspect ratio.

    Returns:
        tuple: (fig, ax) matplotlib figure and axes
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    plt.axis("off")
    return fig, ax

def _save_to_array(fig):
    """Save figure to numpy array.

    Args:
        fig (matplotlib.figure.Figure): The figure to save

    Returns:
        numpy.ndarray: The image as a numpy array
    """
    import io
    import PIL
    import numpy as np

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = PIL.Image.open(buf)
    return np.array(img)

def render(
    *,
    hour: int,
    minute: int,
    second: int,
    face_color: str = "white",
    edge_color: str = "black",
    edge_width: float = 3,
    tick_color: str = "black",
    tick_width: float = 2,
    hour_color: str = "black",
    hour_width: float = 6,
    hour_length: float = 0.5,
    minute_color: str = "black",
    minute_width: float = 3,
    minute_length: float = 0.8,
    second_color: str = "red",
    second_width: float = 1,
    second_length: float = 0.9,
    center_color: str = "black",
    center_size: float = 0.02,
    figure_size: float = 6,
) -> "A_GIS.Code.make_struct":
    """Render a clock face with hour, minute, and seconds hands.

    Args:
        hour (int): Hour value (0-23).
        minute (int): Minute value (0-59).
        second (int): Second value (0-59).
        face_color (str): Color of the clock face.
        edge_color (str): Color of the edge of the clock face.
        edge_width (float): Width of the edge line.
        tick_color (str): Color of the hour ticks.
        tick_width (float): Width of the hour ticks.
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
        figure_size (float): Size of the output figure in inches.

    Returns:
        A_GIS.Code.make_struct: A structure containing:
            - image (numpy.ndarray): The rendered clock face as a numpy array
            - _hour (int): The hour value
            - _minute (int): The minute value
            - _second (int): The second value

    Raises:
        ValueError: If hour, minute, or second are out of valid ranges
        TypeError: If hour, minute, or second are not integers
    """
    import matplotlib.pyplot
    import A_GIS.Code.make_struct
    import A_GIS.Visual.Clock._calculate_hand_angles
    import A_GIS.Visual.Clock._calculate_seconds_angle
    import A_GIS.Visual.Clock._draw_clock_face
    import A_GIS.Visual.Clock._draw_hands
    import A_GIS.Visual.Clock._save_to_array

    # Validate inputs
    if not isinstance(hour, int):
        raise TypeError("hour must be an integer")
    if not isinstance(minute, int):
        raise TypeError("minute must be an integer")
    if not isinstance(second, int):
        raise TypeError("second must be an integer")

    if not (0 <= hour <= 23):
        raise ValueError("hour must be between 0 and 23")
    if not (0 <= minute <= 59):
        raise ValueError("minute must be between 0 and 59")
    if not (0 <= second <= 59):
        raise ValueError("second must be between 0 and 59")

    # Calculate angles
    hour_angle, minute_angle = (
        A_GIS.Visual.Clock._calculate_hand_angles._calculate_hand_angles(
            hour=hour, minute=minute
        )
    )
    seconds_angle = (
        A_GIS.Visual.Clock._calculate_seconds_angle._calculate_seconds_angle(
            seconds=second
        )
    )

    # Create figure
    fig, ax = matplotlib.pyplot.subplots(figsize=(figure_size, figure_size))
    ax.set_aspect("equal")
    matplotlib.pyplot.axis("off")

    # Draw clock face
    A_GIS.Visual.Clock._draw_clock_face._draw_clock_face(
        ax=ax,
        face_color=face_color,
        edge_color=edge_color,
        edge_width=edge_width,
        tick_color=tick_color,
        tick_width=tick_width,
    )

    # Draw hands
    A_GIS.Visual.Clock._draw_hands._draw_hands(
        ax=ax,
        hour_angle=hour_angle,
        minute_angle=minute_angle,
        seconds_angle=seconds_angle,
        hour_color=hour_color,
        hour_width=hour_width,
        hour_length=hour_length,
        minute_color=minute_color,
        minute_width=minute_width,
        minute_length=minute_length,
        second_color=second_color,
        second_width=second_width,
        second_length=second_length,
        center_color=center_color,
        center_size=center_size,
    )

    # Convert to array and clean up
    img_array = A_GIS.Visual.Clock._save_to_array._save_to_array(fig=fig)
    matplotlib.pyplot.close(fig)

    return A_GIS.Code.make_struct(
        image=img_array, _hour=hour, _minute=minute, _second=second
    )
