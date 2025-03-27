import dataclasses

@dataclasses.dataclass
class _Face:
    """Face parameters for clock rendering.

    Attributes:
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
        error: Error message if any validation fails.
    """

    color: str
    edge_color: str
    edge_width: float
    tick_color: str
    tick_width: float
    hour_marker_length: float
    minute_marker_factor: float
    number_font: str
    number_size: float
    number_mode: str
    error: str = ""

    def __post_init__(self):
        if self.edge_width < 0:
            self.error = "Edge width must be >= 0."
        if self.tick_width < 0:
            self.error += " Tick width must be >= 0." if self.error else "Tick width must be >= 0."
        if not (0 <= self.hour_marker_length <= 1):
            self.error += " Hour marker length must be in range [0, 1]." if self.error else "Hour marker length must be in range [0, 1]."
        if self.minute_marker_factor < 0:
            self.error += " Minute marker factor must be >= 0." if self.error else "Minute marker factor must be >= 0."
        if self.number_size <= 0:
            self.error += " Number size must be > 0." if self.error else "Number size must be > 0."
        if self.number_mode not in ['all', 'four', 'none']:
            self.error += " Number mode must be one of: 'all', 'four', 'none'." if self.error else "Number mode must be one of: 'all', 'four', 'none'."
