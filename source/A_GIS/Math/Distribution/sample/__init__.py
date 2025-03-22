import typing

def sample(
    *,
    marginals: typing.List["scipy.stats.rv_continuous"],
    correlation: typing.List[float],
    size: int = 1,
):
    """Generates random samples from correlated marginal distributions

    Each marginal distribution is specified by an instance of the
    scipy.stats.rv_continuous class, and the correlation between them is defined
    through a provided upper triangular correlation matrix. The generated samples
    are returned as a numpy array with one row for each sample, and one column
    for each marginal distribution.

    Args:
        marginals (List[scipy.stats.rv_continuous]): A list of instances of the
            scipy.stats.rv_continuous class representing the marginal distributions
            to be sampled from.
        correlation (numpy.ndarray): An upper triangular correlation matrix as a
            1-D numpy array. It must have length equal to the number of marginals,
            and it is assumed that the diagonal elements are all ones.
        size (int, optional): The number of samples to generate. Defaults to 1.

    Raises:
        ValueError: If the length of the correlation matrix does not match the
            number of marginals.

    Returns:
        numpy.ndarray: A 2-D array where each row represents a generated sample, and
            each column corresponds to a different marginal distribution.
    """

    import scipy
    import numpy
    import A_GIS.Math.CorrelationMatrix.to_numpy

    n = len(marginals)
    if n != correlation.size:
        raise ValueError(
            f"Incorrect size of correlation matrix {
                correlation.size} for the number of marginal distributions {n}."
        )

    # Create the full correlation correlation
    np_matrix = A_GIS.Math.CorrelationMatrix.to_numpy(upper_tri=correlation)

    # Generate correlated normal random variables
    rvs = numpy.random.multivariate_normal(
        numpy.zeros(n), np_matrix, size=size
    )

    # Transform to uniform and then to triangular samples
    unifs = numpy.array([scipy.stats.norm.cdf(row) for row in rvs])
    realizations = numpy.array(
        [[marginals[i].ppf(u[i]) for i in range(n)] for u in unifs]
    )
    return realizations
