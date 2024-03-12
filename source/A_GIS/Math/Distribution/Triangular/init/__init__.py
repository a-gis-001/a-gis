def init(*, low: float, mode: float, high: float):
    """
    Initialize a new triangular distribution.
    """
    import A_GIS.Math.Distribution.Triangular._Triangular

    return A_GIS.Math.Distribution.Triangular._Triangular(low, mode, high)
