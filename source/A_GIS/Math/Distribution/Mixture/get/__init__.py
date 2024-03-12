def get(*, distributions, weights=None, bins=100):
    """Get a mixture of distributions."""
    import numpy

    ndist = len(distributions)
    if weights is None:
        weights = [1.0 / ndist] * ndist

    min_val = distributions[0].low
    max_val = distributions[0].high
    for i in range(1, ndist):
        min_val = min(min_val, distributions[i].low)
        max_val = max(max_val, distributions[i].high)
    x_list = numpy.linspace(min_val, max_val, bins)
    y_list = []
    for x in x_list:
        s = 0
        for i in range(ndist):
            s += weights[i] * distributions[i].pdf(x)
        y_list.append(s)
    return x_list, y_list
