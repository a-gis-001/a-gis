"""Hand parameters for clock rendering."""

import dataclasses

@dataclasses.dataclass
class _Hand:
    """Hand parameters for clock rendering.

    Attributes:
        color: Color of the hand.
        width: Width of the hand.
        length: Length of the hand (0-1 scale).
    """

    color: str
    width: float
    length: float
