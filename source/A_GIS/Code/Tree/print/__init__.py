def print(*, tree, indent=0):
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
