def init_from_file(*, file: type["pathlib.Path"]):
    import A_GIS.Code.Tree._Tree
    import A_GIS.Code.Tree._Visitor
    import A_GIS.File.read
    import A_GIS.Code.Tree.init
    import A_GIS.Code.guess_type
    import A_GIS.Code.Unit.find_root
    if file.is_dir():
        file /= '__init__.py'

    if not file.exists():
        raise ValueError(f"init_from_file: file='{file}' does not exist!")
        
    code = A_GIS.File.read(file=file)    
    _type = A_GIS.Code.guess_type(code=code,file_name=file.name)
    full_name = A_GIS.Code.guess_full_name(file=file)
    name = full_name.split(".")[-1]

    return A_GIS.Code.Tree.init(
        _type=_type, file=file, name=name, full_name=full_name, code=code
    )
