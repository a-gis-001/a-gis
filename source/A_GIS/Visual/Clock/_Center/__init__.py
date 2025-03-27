import dataclasses

@dataclasses.dataclass
class _Center:
    """Center parameters for clock rendering.

    Attributes:
        color: Color of the center circle.
        size: Size of the center circle.
        error: Error message if any validation fails.
    """

    color: str
    size: float
    error: str = ""

    def __post_init__(self):
        if self.size < 0:
            self.error = "Size must be >= 0."
