def sample(*, marginals, correlation, size=1):
    import scipy
    import numpy
    import A_GIS.Math.Statistics.CorrelationMatrix.to_numpy

    n = len(marginals)
    if n != correlation.size:
        raise ValueError(
            f"Incorrect size of correlation matrix {correlation.size} for the number of marginal distributions {n}."
        )

    # Create the full correlation correlation
    np_matrix = A_GIS.Math.Statistics.CorrelationMatrix.to_numpy(upper_tri=correlation)

    # Generate correlated normal random variables
    rvs = numpy.random.multivariate_normal(numpy.zeros(n), np_matrix, size=size)

    # Transform to uniform and then to triangular samples
    unifs = numpy.array([scipy.stats.norm.cdf(row) for row in rvs])
    realizations = numpy.array(
        [[marginals[i].ppf(u[i]) for i in range(n)] for u in unifs]
    )
    return realizations
