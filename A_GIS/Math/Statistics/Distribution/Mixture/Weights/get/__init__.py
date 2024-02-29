def get(*, correlation_matrix, variances, multipliers=None):
    """Get weights based on the correlation matrix and multipliers."""
    import cvxpy
    import numpy
    import A_GIS.Math.Statistics.CorrelationMatrix

    # Construct the covariance matrix from variances and correlations
    corr = A_GIS.Math.Statistics.CorrelationMatrix.to_numpy(
        upper_tri=correlation_matrix
    )
    vcm = numpy.outer(numpy.sqrt(variances), numpy.sqrt(variances)) * corr
    if multipliers is None:
        multipliers = [1.0] * len(variances)

    # Optimization problem
    w = cvxpy.Variable(len(variances))
    objective = cvxpy.Minimize(cvxpy.quad_form(w, vcm))
    constraints = [
        cvxpy.sum(cvxpy.multiply(w, multipliers)) == 1,
        w >= 0,
    ]  # Weights sum to 1 and are non-negative
    prob = cvxpy.Problem(objective, constraints)

    # Solve the problem
    prob.solve()
    return numpy.multiply(w.value, multipliers)
