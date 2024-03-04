def init(*, name="triangular", **kwargs):
    """
    Initialize a new distribution by name.
    """
    import A_GIS.Math.Statistics.Distribution.triangular

    if type == "triangular":
        return A_GIS.Math.Statistics.Distribution.triangular(**kwargs)
    else:
        raise ValueError(f"{type} unknown")
