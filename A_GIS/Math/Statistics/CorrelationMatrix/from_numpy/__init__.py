def from_numpy(*, matrix):
    """Extract the upper triangular values from a NumPy matrix and return a CorrelationMatrix object."""
    import A_GIS.Math.Statistics.CorrelationMatrix.new
    import numpy

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Input must be a square matrix.")

    n = matrix.shape[0]
    upper_tri_indices = numpy.triu_indices(n, k=1)

    # Extract the upper triangular values
    upper_tri_values = matrix[upper_tri_indices]

    # Convert to a list and create a CorrelationMatrix object
    return A_GIS.Math.Statistics.CorrelationMatrix.new(
        size=n, values=upper_tri_values.tolist()
    )
