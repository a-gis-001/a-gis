def split(*, code: str):
    """
    Splits the code into components based on top-level declarations using libcst.

    Args:
        code (str): The Python source code to split.

    Returns:
        dict:
           - names (list): The names of top-level declarations.
           - bodies (list): The corresponding code of the declarations as strings.
    """
    import libcst
    import A_GIS.Code.make_struct

    class TopLevelSplitter(libcst.CSTVisitor):
        def __init__(self, code):
            self.names = []
            self.bodies = []
            self.code = code
            self.current_depth = 0

        def visit_FunctionDef(self, node):
            # Only process top-level functions
            if self.current_depth == 0:
                self.names.append(node.name.value)
                self.bodies.append(self._get_node_code(node))

        def visit_ClassDef(self, node):
            # Only process top-level classes
            if self.current_depth == 0:
                self.names.append(node.name.value)
                self.bodies.append(self._get_node_code(node))

        def _get_node_code(self, node):
            # Extract the source code of the node by reconstructing it as a
            # string
            return libcst.Module([]).code_for_node(node)

        def visit_IndentedBlock(self, node):
            # Increment depth for nested blocks
            self.current_depth += 1

        def leave_IndentedBlock(self, node):
            # Decrement depth after leaving a block
            self.current_depth -= 1

    tree = libcst.parse_module(code)
    splitter = TopLevelSplitter(code)
    tree.visit(splitter)
    return A_GIS.Code.make_struct(names=splitter.names, bodies=splitter.bodies)
