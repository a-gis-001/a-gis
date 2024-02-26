def to_numpy(*, upper_tri):
    """Create a full correlation matrix from an upper triangular data set."""
    import numpy

    n = upper_tri.size
    matrix = numpy.eye(n)  # Start with an identity matrix
    upper_tri_indices = numpy.triu_indices(n, k=1)

    # Assign values to both upper and lower parts of the matrix
    matrix[upper_tri_indices] = upper_tri.values
    matrix[(upper_tri_indices[1], upper_tri_indices[0])] = (
        upper_tri.values  # Mirror the values
    )

    return matrix
