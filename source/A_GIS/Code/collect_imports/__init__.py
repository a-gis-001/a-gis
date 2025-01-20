def collect_imports(*, code: str):
    """
    Extracts top-level imports from Python code using libcst.

    Args:
        code (str): The Python source code.

    Returns:
        list: A list of top-level import statements as strings.
    """
    import libcst

    class TopLevelImportCollector(libcst.CSTVisitor):
        def __init__(self):
            self.imports = []

        def visit_Import(self, node):
            # Collect regular imports
            self.imports.append(self._get_import_string(node))

        def visit_ImportFrom(self, node):
            # Collect 'from ... import ...' statements
            self.imports.append(self._get_import_string(node))

        def _get_import_string(self, node):
            # Reconstruct the source code for the import node
            return libcst.Module([]).code_for_node(node)

    tree = libcst.parse_module(code)
    collector = TopLevelImportCollector()
    tree.visit(collector)
    return collector.imports
