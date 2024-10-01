def _get_dir_root(*, dirname, root):
    """Local function to get the dir and root."""
    import os
    import pathlib

    # We provide the root through an environment variable so we can keep AIs
    # in a local file system, setting the root outside their processes.
    if root is None:
        root = os.getenv("A_GIS_o_File_o_Node_a_root", ".")
    root = pathlib.Path(root)
    dir = root / dirname

    if not root.exists():
        raise ValueError(f"root={root} directory for STACKS node must exist.")
    if not dir.exists():
        raise ValueError(f"dir={dir} directory for STACKS node must exist.")
    if not (root / "_root.node.md").exists():
        raise ValueError(
            f"The root node root={root} does not contain _root.node.md as required to be a root STACKS node."
        )

    return dir, root
