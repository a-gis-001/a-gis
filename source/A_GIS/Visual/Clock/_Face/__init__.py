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
    """

    color: str
    edge_color: str
    edge_width: float
    tick_color: str
    tick_width: float
