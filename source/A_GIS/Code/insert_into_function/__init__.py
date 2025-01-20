def insert_into_function(code, function, add):
    """
    Inserts a code block at the beginning of a function, right after the docstring
    (if it exists) or directly after the function signature.

    Args:
        code (str): The Python source code.
        function (str): The name of the function to modify.
        add (str): The code block to insert.

    Returns:
        str: The modified source code.
    """
    import libcst

    class InsertCodeAfterDocstringTransformer(libcst.CSTTransformer):
        def __init__(self, function, add):
            self.function = function
            self.add = add

        def leave_FunctionDef(self, original_node, updated_node):
            # Check if this is the target function
            if original_node.name.value == self.function:
                # Parse the new code block as a module to handle multi-line
                # additions
                try:
                    code_nodes = libcst.parse_module(self.add).body
                except Exception as e:
                    raise ValueError(
                        f"Invalid code provided for addition: {self.add}"
                    ) from e

                # Get the existing body of the function
                existing_body = updated_node.body.body

                if existing_body:
                    # If the function has an existing body
                    first_statement = existing_body[0]
                    if (
                        isinstance(first_statement, libcst.SimpleStatementLine)
                        and isinstance(first_statement.body[0], libcst.Expr)
                        and isinstance(
                            first_statement.body[0].value, libcst.SimpleString
                        )
                    ):
                        # The first statement is a docstring, insert after it
                        new_body = (
                            [first_statement]
                            + list(code_nodes)
                            + list(existing_body[1:])
                        )
                    else:
                        # No docstring, insert at the very beginning
                        new_body = list(code_nodes) + list(existing_body)
                else:
                    # Function has no body, add the new code block as the
                    # entire body
                    new_body = list(code_nodes)

                # Update the function body
                return updated_node.with_changes(
                    body=libcst.IndentedBlock(body=new_body)
                )

            return updated_node

    # Parse the code
    tree = libcst.parse_module(code)
    transformer = InsertCodeAfterDocstringTransformer(function, add)
    modified_tree = tree.visit(transformer)
    return modified_tree.code
