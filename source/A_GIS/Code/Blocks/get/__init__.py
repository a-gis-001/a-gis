def get(*, code=""):
    """Split the code into blocks"""
    import A_GIS.Code.Docstring.modify

    c = A_GIS.Code.Docstring.modify(code=code, docstring=None)
    l = c.split("\n")
    c2 = []
    for x in l:
        c2.append(x.rstrip())

    c3 = []
    start_fun = False
    end_fun = False
    for x in c2:
        if start_fun and end_fun:
            c3.append(x)
        if x.startswith("def"):
            start_fun = True
        if start_fun and x.endswith(":"):
            end_fun = True

    blocks = []
    y = []
    for x in c3:
        if x == "":
            if len(y) > 0:
                blocks.append(y)
            y = []
        else:
            y.append(x)
    return blocks
