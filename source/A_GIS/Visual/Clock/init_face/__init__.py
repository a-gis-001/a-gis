def init_face(
    *,
    color: str = "white",
    edge_color: str = "black",
    edge_width: float = 3,
    tick_color: str = "black",
    tick_width: float = 2,
) -> "A_GIS.Visual.Clock._Face":
    """Initialize face parameters for clock rendering.

    Args:
        color: Color of the clock face.
        edge_color: Color of the edge of the clock face.
        edge_width: Width of the edge line.
        tick_color: Color of the hour ticks.
        tick_width: Width of the hour ticks.

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
    )
