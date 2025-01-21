def absorb(*, code: str, name: str = None, write: bool = True):
    """Absorb code into A_GIS

    If name is None then generate a name.

    """
    import A_GIS.Code.pack_into_function
    import A_GIS.File.write
    import A_GIS.Code.Unit.Name.check
    import A_GIS.Code.make_struct

    path = None
    new_name = None
    found_name = False
    generated_names = None
    error = None
    if name:
        new_name = A_GIS.Code.Unit.Name.fix(name=name, unit_type="function")
        path = A_GIS.Code.Unit.Name.to_path(name=new_name, check_exists=False)
        found_name = not path.exists()

    # Generate names if the user did not pass them in or the one they passed
    # was used.
    if not found_name:
        x = A_GIS.Code.Unit.Name.generate(description=code)
        generated_names = x.names
        if len(generated_names) == 0:
            error = "No names returned by AI for this code!"
        else:
            for n in generated_names:
                new_name = A_GIS.Code.Unit.Name.fix(
                    name=n, unit_type="function"
                )
                new_function = new_name.split(".")[-1]
                path = A_GIS.Code.Unit.Name.to_path(
                    name=new_name, check_exists=False
                )
                if not path.exists():
                    found_name = True
                    break
            if not found_name:
                error = f"No names provided by AI {names} are valid. All paths already exist!"

    new_function = None
    old_function = None
    new_code = None
    packed_code = None
    renamed_code = None
    if found_name:

        new_function = new_name.split(".")[-1]

        x = A_GIS.Code.pack_into_function(code=code)
        old_function = x._function
        packed_code = x.code

        renamed_code = A_GIS.Code.rename_function(
            code=packed_code, old=old_function, new=new_function
        )

        new_code = A_GIS.Code.reformat(code=renamed_code)

        if write:
            path = A_GIS.Code.Unit.touch(name=new_name)
            A_GIS.File.write(content=new_code, file=path)

    return A_GIS.Code.make_struct(
        _name=name,
        _write=write,
        _code=code,
        generated_names=generated_names,
        path=path,
        name=new_name,
        function=new_function,
        old_function=old_function,
        code=new_code,
        renamed_code=renamed_code,
        packed_code=packed_code,
        error=error,
    )
