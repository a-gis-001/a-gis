def to_string(
    *,
    tree: type["A_GIS.Code.Tree._Tree"],
    indent_chars: str = "....",
    indent: int = 0,
):
    """Converts a Tree object into a formatted string representation.

    This function recursively traverses the given tree structure and generates a
    human-readable string representation of it. Each node in the tree is represented
    as an indented line, with its type and name displayed. The depth of indentation
    increases for each level of nesting.

    Args:
        tree (A_GIS.Code.Tree._Tree): The Tree object to be converted into a string.
        indent_chars (str, optional): A string used for indentation in the output string.
                                       Defaults to "....".
        indent (int, optional): An integer representing the current level of indentation.
                               It is incremented at each recursive call. Defaults to 0.

    Raises:
        None

    Returns:
        str: A string representation of the Tree object. Each line represents a node in the tree,
             and nodes are indented according to their depth in the tree structure.
    """

    s = ""
    if tree._type != "":
        s = f"{indent_chars * indent} {indent:02d} {tree._type} {tree.name}\n"
        indent += 1
    for k, v in tree.children.items():
        s += to_string(tree=v, indent_chars=indent_chars, indent=indent)
    return s
