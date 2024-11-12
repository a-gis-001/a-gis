import re

def get(
    *,
    code: str,
    ignore_class=re.compile("^__"),
    ignore_function=re.compile("^__"),
) -> dict:
    """Extract a hierarchical structure of Python code.

    This function takes a string containing Python code and returns a
    dictionary representing the hierarchy of classes and functions
    defined in the code. It uses the `ast` module to parse the code and
    traverses the abstract syntax tree (AST) to build the hierarchy.
    Classes and functions that match the provided regular expression
    patterns (`ignore_class` and `ignore_function`) are ignored.

    Args:
        code (str):
            A string containing Python code to be parsed.
        ignore_class (re.Pattern, optional):
            A compiled regular expression pattern used to ignore classes
            whose names match this pattern. Defaults to ignoring all
            classes starting with double underscores.
        ignore_function (re.Pattern, optional):
            A compiled regular expression pattern used to ignore
            functions whose names match this pattern. Defaults to
            ignoring all functions starting with double underscores.

    Returns:
        dict:
            A dictionary representing the hierarchical structure of
            classes and functions in the provided code. The dictionary
            includes an "_imports" key listing all imported modules or
            objects.
    """
    import ast

    class __HierarchyVisitor(ast.NodeVisitor):
        def __init__(self):
            self.hierarchy = {}
            self.current_scope = self.hierarchy
            self.hierarchy["_imports"] = []

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

        def visit_Import(self, node):
            for alias in node.names:
                self.hierarchy["_imports"].append(alias.name)

        def visit_ImportFrom(self, node):
            module = node.module if node.module else ""
            for alias in node.names:
                import_name = f"{module}.{alias.name}" if module else alias.name
                self.hierarchy["_imports"].append(import_name)

    nodes = ast.parse(code)
    hierarchy_visitor = __HierarchyVisitor()
    hierarchy_visitor.visit(nodes)

    return hierarchy_visitor.hierarchy
