def init(*, name="triangular", **kwargs):
    """
    Initialize a new distribution by name.
    """
    import A_GIS.Math.Distribution.Triangular.init

    if type == "triangular":
        return A_GIS.Math.Distribution.Triangular.init(**kwargs)
    else:
        raise ValueError(f"{type} unknown")
