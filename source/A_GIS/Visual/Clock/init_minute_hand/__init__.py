"""Initialize minute hand parameters for clock rendering."""

def init_minute_hand(
    *,
    color: str = "black",
    width: float = 3,
    length: float = 0.8,
) -> "A_GIS.Visual.Clock._Hand":
    """Initialize minute hand parameters for clock rendering.

    Args:
        color: Color of the minute hand.
        width: Width of the minute hand.
        length: Length of the minute hand (0-1 scale).

    Returns:
        A_GIS.Visual.Clock._Hand: Minute hand parameters.
    """
    import A_GIS.Visual.Clock._Hand

    return A_GIS.Visual.Clock._Hand(
        color=color,
        width=width,
        length=length,
    )
