def update_and_show_git_status(*, root: type["pathlib.Path"]):
    """Update all the files, doing formatting and performing checks"""
    import A_GIS.Cli.get_git_status
    import A_GIS.Code.Tree.update

    # Update the the tree.
    tree = A_GIS.Code.Tree.recurse(path=root)
    A_GIS.Code.Tree.update(tree=tree)

    # Return what has changed in the root directory as a panel.
    panel = A_GIS.Cli.get_git_status(root=root)
    return panel
