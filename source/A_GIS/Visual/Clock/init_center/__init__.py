"""Initialize center parameters for clock rendering."""

def init_center(
    *,
    color: str = "black",
    size: float = 0.02,
) -> "A_GIS.Visual.Clock._Center":
    """Initialize center parameters for clock rendering.

    Args:
        color: Color of the center circle.
        size: Size of the center circle.

    Returns:
        A_GIS.Visual.Clock._Center: Center parameters.
    """
    import A_GIS.Visual.Clock._Center

    return A_GIS.Visual.Clock._Center(
        color=color,
        size=size,
    )
