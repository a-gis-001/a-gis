def _make_result(
    *,
    image,
    error: str,
    hour: int,
    minute: int,
    second: int,
    face: "A_GIS.Visual.Clock._Face",
    hour_hand: "A_GIS.Visual.Clock._Hand",
    minute_hand: "A_GIS.Visual.Clock._Hand",
    second_hand: "A_GIS.Visual.Clock._Hand",
    center: "A_GIS.Visual.Clock._Center",
    figure_size: float,
) -> "A_GIS.Code.make_struct":
    """Create the result struct with all parameters.

    Args:
        image: The rendered clock face as a numpy array or None
        error: Error message if any
        hour: Hour value (0-23)
        minute: Minute value (0-59)
        second: Second value (0-59)
        face: Face parameters
        hour_hand: Hour hand parameters
        minute_hand: Minute hand parameters
        second_hand: Second hand parameters
        center: Center parameters
        figure_size: Size of the output figure in inches

    Returns:
        A_GIS.Code.make_struct: A structure containing all parameters
    """
    import A_GIS.Code.make_struct

    return A_GIS.Code.make_struct(
        image=image,
        error=error,
        _hour=hour,
        _minute=minute,
        _second=second,
        _face=face,
        _hour_hand=hour_hand,
        _minute_hand=minute_hand,
        _second_hand=second_hand,
        _center=center,
        _figure_size=figure_size,
    )
