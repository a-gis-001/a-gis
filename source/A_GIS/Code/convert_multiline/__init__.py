def convert_multiline(*, code: str) -> str:
    """Convert multiline strings to a canonical form using LibCST.

    Args:
        code (str): The Python source code to convert.
    """
    import libcst
    import textwrap
    import re

    class MultilineStringTransformer(libcst.CSTTransformer):
        def leave_SimpleString(self, original_node, updated_node):
            # Check if string is triple doubles or singles
            new_value = updated_node.value.encode("utf-8").decode(
                "unicode_escape"
            )
            ts = new_value.startswith("'''") and new_value.endswith("'''")
            td = new_value.startswith('"""') and new_value.endswith('"""')

            if ts or td:
                return updated_node.with_changes(value=new_value)

            return updated_node

    # Parse the source code into a LibCST Module
    tree = libcst.parse_module(code)

    # Transform the CST
    wrapper = libcst.MetadataWrapper(tree)
    transformed_tree = wrapper.visit(MultilineStringTransformer())

    # Convert the CST back into a code string
    return transformed_tree.code
