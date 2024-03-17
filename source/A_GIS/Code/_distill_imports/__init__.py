def _distill_imports(*, code: str) -> str:
    """
    Canonicalize import statements

    Change "as" versions to their absolute version and replaces
    function calls within the body to use the absolute path.

    Note this removes comments and docstrings so should only be used when you are doing
    a destructive operation like `distill`.

    Args:
        code (str): The Python code to transform.

    Returns:
        str: The transformed Python code.
    """
    import ast
    import astunparse

    class ImportCallTransformer(ast.NodeTransformer):
        def __init__(self):
            self.alias_map = {}

        def visit_Import(self, node):
            for alias in node.names:
                if alias.asname:
                    self.alias_map[alias.asname] = alias.name
                    alias.asname = None
            return node

        def visit_ImportFrom(self, node):
            for alias in node.names:
                if alias.asname:
                    full_name = f"{node.module}.{alias.name}"
                    self.alias_map[alias.asname] = full_name
                    alias.name = full_name
                    alias.asname = None
            return node

        def visit_Attribute(self, node):
            self.generic_visit(node)
            if (
                isinstance(node.value, ast.Name)
                and node.value.id in self.alias_map
            ):
                return ast.copy_location(
                    ast.Attribute(
                        value=ast.Name(
                            id=self.alias_map[node.value.id], ctx=ast.Load()
                        ),
                        attr=node.attr,
                        ctx=node.ctx,
                    ),
                    node,
                )
            return node

        def visit_Name(self, node):
            if node.id in self.alias_map:
                return ast.copy_location(
                    ast.Name(id=self.alias_map[node.id], ctx=node.ctx), node
                )
            return self.generic_visit(node)

    tree = ast.parse(code)
    transformer = ImportCallTransformer()
    transformed_tree = transformer.visit(tree)

    return astunparse.unparse(transformed_tree)
