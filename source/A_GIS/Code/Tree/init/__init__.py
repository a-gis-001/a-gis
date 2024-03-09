def init(*, code: str, _type="", file="", name="", full_name="", root=""):
    import A_GIS.Code.Tree._Tree
    import A_GIS.Code.Tree._Visitor
    import A_GIS.Text.hash
    import libcst

    # Do the work.
    visitor = A_GIS.Code.Tree._Visitor(root=root)
    tree = libcst.parse_module(code)
    visitor.current_file = file
    tree.visit(visitor)

    # Populate the data structure.
    return A_GIS.Code.Tree._Tree(
        _type=_type,
        file=file,
        name=name,
        full_name=full_name,
        body=code,
        hash=A_GIS.Text.hash(text=code),
        children=visitor.structure,
    )
