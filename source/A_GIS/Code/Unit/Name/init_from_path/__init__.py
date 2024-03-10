def init_from_path(*, path: type["pathlib.Path"]):
    """Initialize an A_GIS functional code unit from a path"""
    import A_GIS.Code.guess_name
    import A_GIS.Code.Unit.Name.check

    name = A_GIS.Code.guess_name(path=path)
    if not A_GIS.Code.Unit.Name.check(name=name):
        raise ValueError(
            f"Name {name} derived from {path} does not satisfy A_GIS standard!"
        )

    return name
