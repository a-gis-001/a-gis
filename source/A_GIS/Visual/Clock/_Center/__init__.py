"""Center parameters for clock rendering."""

import dataclasses

@dataclasses.dataclass
class _Center:
    """Center parameters for clock rendering.

    Attributes:
        color: Color of the center circle.
        size: Size of the center circle.
    """

    color: str
    size: float
