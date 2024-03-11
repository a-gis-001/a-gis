def print(*, tree, indent=0):
    """Prints a tree of code elements in Markdown format with optional indentation levels.

    This function recursively processes the provided `tree` dictionary, generating a formatted string
    representing the structure and types of the items within. The resulting output is formatted as
    a Markdown list, where each item represents a node in the tree and its children are nested under it.

    Args:
        tree (dict): A dictionary representation of a code element tree to be printed. Each key-value pair
                      in the dictionary represents an item in the tree, with the key being the name of the
                      item and the value being another dictionary representing nested items or a string
                      representing the type of the item.
        indent (int, optional): The number of levels to indent the output for each recursive call. Each level
                                represents 4 spaces in the output. Defaults to 0.
    Raises:
        None

    Returns:
        str: A string representing the formatted code element tree in Markdown format with optional indentation.
    """

    import A_GIS.Code.Tree.print

    markdown = ""
    indent_str = "    " * indent  # 4 spaces for each indentation level

    for key, value in tree.items():
        if key == "_type" or key == "_file":
            continue
        markdown += f"{indent_str}- {value['_type']} {key}\n"

        # Recursively process nested items
        if isinstance(value, dict) and value:
            markdown += A_GIS.Code.Tree.print(tree=value, indent=indent + 1)

    return markdown
