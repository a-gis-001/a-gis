def init_from_path(*, path: type["pathlib.Path"]):
    """Initialize an A_GIS functional code unit from a path"""
    import A_GIS.Code.guess_name
    import A_GIS.Code.guess_type
    import A_GIS.Code.Unit.Name.check

    path = path.resolve()
    name = A_GIS.Code.guess_name(path=path)
    unit_type = A_GIS.Code.guess_type(file=path)
    check = A_GIS.Code.Unit.Name.check(name=name, unit_type=unit_type)
    if not check.result:
        raise ValueError(
            f"Name {name} derived from {path} does not correspond to A_GIS {unit_type} unit (fixed_name={check.fixed_name})!"
        )

    return name
