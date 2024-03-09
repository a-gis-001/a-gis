import libcst

class _Visitor(libcst.CSTVisitor):

    def __init__(self, root):
        self.stack = [root]
        self.structure = {}
        # Keep track of the current position in the hierarchy
        self.current_structure = self.structure

    def visit_Any(self, type, node):
        import A_GIS.Code.Tree._Tree
        import A_GIS.Text.hash

        name = node.name.value
        self.stack.append(name)

        original_structure = self.current_structure

        code = libcst.Module([node]).code
        self.current_structure[name] = A_GIS.Code.Tree._Tree(
            **{
                "_type": type,
                "file": self.current_file,
                "name": name,
                "full_name": ".".join(self.stack),
                "body": code,
                "hash": A_GIS.Text.hash(text=code),
                "children": {},
            }
        )

        # Move into the class's scope in the hierarchy
        self.current_structure = self.current_structure[name].children
        for element in node.body.body:
            if isinstance(
                element, (libcst.FunctionDef, libcst.ClassDef)
            ):  # Extendable to other types
                element.visit(self)

        # Restore the structure back to the parent's scope after finishing with
        # the class
        self.current_structure = original_structure
        self.stack.pop()
        return False

    def visit_FunctionDef(self, node: libcst.FunctionDef) -> None:
        return self.visit_Any("function", node)

    def visit_ClassDef(self, node: libcst.ClassDef) -> None:
        return self.visit_Any("class", node)
