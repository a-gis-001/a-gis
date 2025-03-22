def _process_args_name_code(*, name, code):
    import A_GIS.Code.Unit.read

    if code is None and name is None:
        raise ValueError("Either 'code' or 'name' must be specified.")
    if code is not None and name is not None:
        raise ValueError("Specify either 'code' or 'name', not both.")
    if name is not None:
        code = A_GIS.Code.Unit.read(name=name).code
    return name, code
