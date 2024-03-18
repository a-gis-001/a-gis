def convert_multiline(*, code: str):
    """
    Reads a Python file, converts all its string literals to use triple-quoted strings
    where appropriate, and writes the modified code back to the file.

    Args:
        filename (str): The path to the Python file to convert.
    """
    import ast
    import astor

    class __StringConverter(ast.NodeTransformer):
        """
        An AST node transformer that converts all string literals in the code
        to triple-quoted strings if they contain newlines, or maintains them
        as single or double-quoted strings if they don't contain newlines but
        ensuring consistency.
        """

        def visit_Str(self, node):
            # This method will visit every string in the code.
            if "\n" in node.s:
                # For multiline strings, use triple double quotes and escape
                # existing triple quotes
                new_s = '"""' + node.s.replace('"""', '\\"""') + '"""'
            else:
                # For single line strings, just ensure they're using double
                # quotes for consistency
                new_s = '"' + node.s.replace('"', '\\"') + '"'

            return ast.Str(s=new_s)

        def visit_Bytes(self, node):
            # Similar logic can be applied to bytes if needed, or customize as
            # required.
            return node

    # Parse the source code into an AST
    tree = ast.parse(code)

    # Transform the AST
    converter = __StringConverter()
    converted_tree = converter.visit(tree)

    return astor.to_source(converted_tree)
