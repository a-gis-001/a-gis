def triangular(*, low: float, mode: float, high: float):
    """
    Initialize a new triangular distribution.
    """
    import A_GIS.Math.Statistics.Distribution._Triangular

    return A_GIS.Math.Statistics.Distribution._Triangular(low, mode, high)
