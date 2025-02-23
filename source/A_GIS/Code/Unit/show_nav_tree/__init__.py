def show_nav_tree(*, nav_history, root="A_GIS"):
    """Display navigation history as a tree"""
    import rich.tree
    import importlib
    import inspect

    tree = rich.tree.Tree(root, style="bold", guide_style="bold bright_black")
    current_nodes = {root: tree}

    for path, type_, obj in nav_history:
        parts = path.split(".")
        current = root

        for part in parts[1:]:
            parent = current
            current = f"{current}.{part}"
            last = part == parts[-1]
            if current not in current_nodes:
                try:
                    if last and type_ in ("function", "class"):
                        style = "cyan" if type_ == "function" else "magenta"
                        doc = inspect.getdoc(obj)
                        desc = "  # " + doc.split("\n")[0]
                    else:
                        style = "green"
                        module = importlib.import_module(current)
                        doc = inspect.getdoc(module)
                        desc = "  # " + doc.split("\n")[0]
                except BaseException:
                    desc = ""
                label = f"{part}{desc}"
                current_nodes[current] = current_nodes[parent].add(
                    label, style=style, guide_style="bold bright_black"
                )

    return tree
