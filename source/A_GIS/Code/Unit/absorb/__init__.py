def absorb(*, code: str, name: str, move: bool = True):
    """Absorb code into A_GIS

    If name is None then generate a name.

    """
    import A_GIS.Code.pack_into_function
    import A_GIS.File.read
    import A_GIS.Code.Unit.Name.check

    fixed_name = A_GIS.Code.Unit.Name.fix(name=name, unit_type="function")
    new_name = fixed_name.split(".")[-1]

    x = A_GIS.Code.pack_into_function(code=code)
    old_name = x._function
    packed_code = x.code

    return A_GIS.Code.rename_function(
        code=packed_code, old=old_name, new=new_name
    )
