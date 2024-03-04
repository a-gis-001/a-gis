def init(*, type="triangular", **kwargs):
    """
    Initialize a new distribution.
    """
    import A_GIS.Math.Statistics.Distribution._Triangular

    if type == "triangular":
        return A_GIS.Math.Statistics.Distribution._Triangular(**kwargs)
    else:
        raise ValueError(f"{type} unknown")
