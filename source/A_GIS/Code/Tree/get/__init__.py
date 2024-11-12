import re

def get(
    *,
    code: str,
    ignore_class=re.compile("^__"),
    ignore_function=re.compile("^__"),
) -> dict:
    """Extract Python code hierarchy of classes and functions.

    This function takes a string containing Python code and returns a
    nested dictionary representing the hierarchy of classes and
    functions defined in the code. The hierarchy is constructed by
    traversing the abstract syntax tree (AST) of the code using a custom
    `NodeVisitor` class. Classes and functions that match the provided
    regular expressions are ignored during this process.

    Args:
        code (str):
            A string containing Python code to be parsed.
        ignore_class (re.Pattern, optional):
            A compiled regular expression pattern used to filter out
            classes from the hierarchy. Defaults to `re.compile("^__")`,
            which ignores all classes starting with double underscores.
        ignore_function (re.Pattern, optional):
            A compiled regular expression pattern used to filter out
            functions from the hierarchy. Defaults to
            `re.compile("^__")`, which ignores all functions starting
            with double underscores.

    Returns:
        dict:
            A nested dictionary representing the hierarchical structure
            of classes and functions in the provided code. Each class
            and function is represented as a key in the dictionary, with
            its value being another dictionary containing its type
            (`_type`) and any nested structures.
    """
    import ast

    class __HierarchyVisitor(ast.NodeVisitor):
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
    hierarchy_visitor = __HierarchyVisitor()
    hierarchy_visitor.visit(nodes)

    return hierarchy_visitor.hierarchy
