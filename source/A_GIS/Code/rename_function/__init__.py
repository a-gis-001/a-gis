def rename_function(*, code: str, old: str, new: str):
    """Renames a single function within the code."""
    import libcst

    class RenameFunctionTransformer(libcst.CSTTransformer):
        def __init__(self, old_name, new_name):
            self.old_name = old_name
            self.new_name = new_name

        def leave_FunctionDef(self, original_node, updated_node):
            # Check if the function name matches the one to be renamed
            if original_node.name.value == self.old_name:
                return updated_node.with_changes(
                    name=libcst.Name(self.new_name)
                )
            return updated_node

        def leave_Call(self, original_node, updated_node):
            # Update calls to the renamed function
            if (
                isinstance(original_node.func, libcst.Name)
                and original_node.func.value == self.old_name
            ):
                return updated_node.with_changes(
                    func=libcst.Name(self.new_name)
                )
            return updated_node

    # Parse the code into a libcst
    module = libcst.parse_module(code)

    # Apply the transformer
    transformer = RenameFunctionTransformer(old, new)
    modified_module = module.visit(transformer)

    # Return the transformed code as a string
    return modified_module.code
