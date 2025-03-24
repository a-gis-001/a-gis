"""Initialize hour hand parameters for clock rendering."""

def init_hour_hand(
    *,
    color: str = "black",
    width: float = 6,
    length: float = 0.2,  # 0.4 * 0.5
) -> "A_GIS.Visual.Clock._Hand":
    """Initialize hour hand parameters for clock rendering.

    Args:
        color: Color of the hour hand.
        width: Width of the hour hand.
        length: Length of the hour hand (0-1 scale).

    Returns:
        A_GIS.Visual.Clock._Hand: Hour hand parameters.
    """
    import A_GIS.Visual.Clock._Hand

    return A_GIS.Visual.Clock._Hand(
        color=color,
        width=width,
        length=length,
    )
