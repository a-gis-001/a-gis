def main():
    import A_GIS.Code.Unit.Name.init_from_path
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.File.read
    import sys
    import A_GIS.Code.Docstring.generate
    import A_GIS.Code.replace_docstring
    import pathlib
    import A_GIS.File.write

    path = sys.argv[1]
    if "." in path:
        name = path
        path = A_GIS.Code.Unit.Name.to_path(name=name) / "__init__.py"
    else:
        path = pathlib.Path(path)
        name = A_GIS.Code.Unit.Name.init_from_path(path=path)
        if path.is_dir():
            path /= "__init__.py"
    print("path:", path)
    print("name:", name)

    code = A_GIS.File.read(file=path)
    docstring = A_GIS.Code.Docstring.generate(name=name, code=code)
    print("docstring:\n", docstring)

    #code = A_GIS.Code.replace_docstring(code=code, docstring=docstring)
    #A_GIS.File.write(content=code, file=path)


if __name__ == "__main__":
    main()
