def init_second_hand(
    *,
    color: str = "red",
    width: float = 1,
    length: float = 0.9,
) -> "A_GIS.Visual.Clock._Hand":
    """Initialize second hand parameters for clock rendering.

    Args:
        color: Color of the second hand.
        width: Width of the second hand.
        length: Length of the second hand (0-1 scale).

    Returns:
        A_GIS.Visual.Clock._Hand: Second hand parameters.
    """
    import A_GIS.Visual.Clock._Hand

    return A_GIS.Visual.Clock._Hand(
        color=color,
        width=width,
        length=length,
    )
