def to_string(
    *,
    tree: type["A_GIS.Code.Tree._Tree"],
    indent_chars: str = "....",
    indent: int = 0,
):
    s = ""
    if tree._type != "":
        s = f"{indent_chars * indent} {indent:02d} {tree._type} {tree.name}\n"
        indent += 1
    for k, v in tree.children.items():
        s += to_string(tree=v, indent_chars=indent_chars, indent=indent)
    return s
