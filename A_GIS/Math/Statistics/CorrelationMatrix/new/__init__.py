import typing


def new(
    *, size: int = 1, values: typing.Optional[typing.List[float]] = []
):
    """
    Return a correlation matrix data class from the upper triangular values.

    This function initializes a `_CorrMatrix` data class with a specified size and set of values.
    The values are expected to represent the upper triangular part of the matrix.

    Args:
        size (int): The size of the correlation matrix. Defaults to 1.
        values (Optional[List[float]]): A list of float values to initialize the matrix. Must represent the upper triangular part of the matrix. If None, initializes with zeros.

    Returns:
        _CorrMatrix: An instance of the `_CorrMatrix` data class.

    Raises:
        ValueError: If the number of values provided does not match the expected count for the upper triangular part of the matrix.

    Example:
        # Example of initializing a 3x3 correlation matrix
        matrix = new(size=3, values=[0.1, 0.2, 0.3])

    """
    import dataclasses
    import typing

    @dataclasses.dataclass
    class _CorrMatrix:
        size: int
        values: typing.List[float]

        def __post_init__(self):
            nv = len(self.values)
            nc = self.size * (self.size - 1) / 2
            if nv != nc:
                raise ValueError(
                    f"Invalid number of values {nv} for the correlation coefficients for the matrix size={self.size}. Should be {nc}."
                )

        def __repr__(self):
            return f"A_GIS.Math.Statistics.CorrelationMatrix.new(size={size},values={values})"

    return _CorrMatrix(size, values)
