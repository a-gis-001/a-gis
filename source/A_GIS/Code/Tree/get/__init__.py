import re


def get(
    *, code: str, ignore_class=re.compile("^_"), ignore_function=re.compile("^_")
) -> dict:
    """Get a code tree from a code string."""
    import ast

    class _HierarchyVisitor(ast.NodeVisitor):
        def __init__(self):
            self.hierarchy = {}
            self.current_scope = self.hierarchy

        def visit_ClassDef(self, node):
            if ignore_class.match(node.name):
                return
            class_name = node.name
            previous_scope = self.current_scope
            self.current_scope = self.current_scope.setdefault(
                class_name, {"_type": "class"}
            )
            for child_node in node.body:
                self.visit(child_node)
            self.current_scope = previous_scope

        def visit_FunctionDef(self, node):
            if ignore_function.match(node.name):
                return
            function_name = node.name
            previous_scope = self.current_scope
            self.current_scope[function_name] = {"_type": "function"}
            self.current_scope = self.current_scope[function_name]
            for child_node in node.body:
                self.visit(child_node)
            self.current_scope = previous_scope

    nodes = ast.parse(code)
    hierarchy_visitor = _HierarchyVisitor()
    hierarchy_visitor.visit(nodes)

    return hierarchy_visitor.hierarchy
