def convert_multiline(*, code: str):
    """Convert multiline strings to a canonical form

    Args:
        code (str): The path to the Python file to convert.
    """
    import ast
    import astor
    import io
    import re
    import textwrap

    # This prefix is used to indent the nodes
    _prefix = '--convert_multiline' * 4
    
    class StringTransformer(ast.NodeTransformer):
        # This method will visit every string in the code.
        def visit_Str(self, node):
            
            had_newline = "\n" in node.s

            output = io.StringIO()
            print(node.s, file=output, end='')
            node.s = output.getvalue()
            output.close()

            if had_newline:
                triple_singles="'''"
                triple_doubles='"""'
                if node.s.find(triple_doubles)>=0:
                    node.s = node.s.replace(triple_doubles,triple_singles)
                node.s = textwrap.indent(node.s,_prefix)

            return node

    # Parse the source code into an AST
    tree = ast.parse(code)

    # Transform the AST
    converter = StringTransformer()
    converted_tree = converter.visit(tree)

    source = astor.to_source(converted_tree)
    source,_ = re.subn('^'+_prefix,'',source,flags=re.MULTILINE)
    return source
