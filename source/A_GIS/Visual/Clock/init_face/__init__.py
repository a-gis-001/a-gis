def init_face(
    *,
    color: str = "white",
    edge_color: str = "black",
    edge_width: float = 3,
    tick_color: str = "black",
    tick_width: float = 2,
    hour_marker_length: float = 0.1,
    minute_marker_factor: float = 0.5,
    number_font: str = "Arial",
    number_size: float = 0.1,
    number_mode: str = "none",
) -> "A_GIS.Visual.Clock._Face":
    """Initialize face parameters for clock rendering.

    Args:
        color: Color of the clock face.
        edge_color: Color of the edge of the clock face.
        edge_width: Width of the edge line.
        tick_color: Color of the hour ticks.
        tick_width: Width of the hour ticks.
        hour_marker_length: Length of hour markers (0-1).
        minute_marker_factor: Factor for minute marker length (0 to disable).
        number_font: Font for hour numbers.
        number_size: Size of hour numbers.
        number_mode: Mode for displaying numbers ('all', 'four', 'none').

    Returns:
        A_GIS.Visual.Clock._Face: Face parameters.
    """
    import A_GIS.Visual.Clock._Face

    return A_GIS.Visual.Clock._Face(
        color=color,
        edge_color=edge_color,
        edge_width=edge_width,
        tick_color=tick_color,
        tick_width=tick_width,
        hour_marker_length=hour_marker_length,
        minute_marker_factor=minute_marker_factor,
        number_font=number_font,
        number_size=number_size,
        number_mode=number_mode,
    )
