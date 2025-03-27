import dataclasses

@dataclasses.dataclass
class _Hand:
    """Hand parameters for clock rendering.

    Attributes:
        color: Color of the hand.
        width: Width of the hand (must be >= 0).
        length: Length of the hand (must be in the range [0, 1]).
        error: Error message if any validation fails.
    """

    color: str
    width: float
    length: float
    error: str = ""

    def __post_init__(self):
        if not (0 <= self.length <= 1):
            self.error = "Length must be in the range [0, 1]."
        if self.width < 0:
            self.error = "Width must be >= 0."
            if self.error:  # If there's already an error, append the new one
                self.error += " "
            self.error += "Width must be >= 0."
