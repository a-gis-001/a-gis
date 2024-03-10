def check(*, name: str):
    """Check the name for standards."""
    import A_GIS.Code.Unit.Name.fix

    return A_GIS.Code.Unit.Name.fix(name=name) == name
