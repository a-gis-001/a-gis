def get_context(*, dirname: str, _root: str = None):
    """Retrieve contextual documentation for a directory hierarchy.

    This function constructs the context by traversing up from a target
    directory, collecting documentation for each level (root, trunk,
    branch, and leaf). It returns a structured object containing error
    information, text content for each level, and the directory paths.
    The structure is created using `A_GIS.Code.make_struct`.

    Args:
        dirname (str):
            The name of the target directory to start from. If `None`,
            no context will be generated.
        _root (str, optional):
            An optional path representing the root of the hierarchy. If
            `None`, the function will attempt to determine the root.

    Returns:
        dataclass:
            A structured object with the following attributes:

            - error (Optional[str]): A string describing any error
              encountered during processing.
            - root_text (str): The text content of the root
              documentation file.
            - root_reldir (str): The relative path from the target
              directory to the root directory.
            - branch_text (Optional[str]): The text content of the
              branch documentation file, if available.
            - branch_dir (Optional[str]): The relative path from the
              target directory to the branch directory, if available.
            - trunk_texts (List[str]): A list of text contents for
              each trunk documentation file in descending order of
              hierarchy level.
            - trunk_dirs (List[str]): A list of relative paths from
              the target directory to each trunk directory in
              descending order of hierarchy level.
            - trunk_dir (Optional[str]): The relative path from the
              target directory to the topmost trunk directory, if
              available.
            - leaf_text (Optional[str]): The text content of the leaf
              documentation file, if available.
            - leaf_dir (Optional[str]]: The relative path from the
              target directory to the leaf directory, if available.
            - context (str): A formatted string containing all the
              documentation levels in Markdown format, with headings
              for each level.
    """
    import A_GIS.Code.make_struct
    import A_GIS.File.read
    import A_GIS.File.Node._get_dir_root

    # Get the target directory and root_dir directory.
    target_dir, root_dir = A_GIS.File.Node._get_dir_root(
        dirname=dirname, root=_root
    )

    # Initialize variables.
    trunk_dirs = []
    trunk_dir = None
    trunk_texts = []
    trunk_text = None

    leaf_dir = None
    leaf_text = None

    branch_dir = None
    branch_text = None

    root_reldir = None
    root_text = None

    error = None
    context = None
    names = ["root", "trunk", "branch", "leaf"]
    try:

        # Traverse the directories from bottom to top (root_dir).
        dir = target_dir
        level = 4
        while dir.parent != root_dir:

            # First we could hit a leaf.
            target_file = dir / "_leaf.node.md"
            if target_file.exists():
                if level <= 3:
                    raise ValueError(
                        f"Problem with leaf directory {dir}. A leaf cannot be above a {names[level]} node."
                    )
                level = 3
                leaf_dir = str(dir.relative_to(root_dir))
                leaf_text = A_GIS.File.read(file=target_file)

            # Then we could hit a branch.
            target_file = dir / "_branch.node.md"
            if target_file.exists():
                if level <= 2:
                    raise ValueError(
                        f"Problem with branch directory {dir}. A branch cannot be above a {names[level]} node."
                    )
                level = 2
                branch_dir = str(dir.relative_to(root_dir))
                branch_text = A_GIS.File.read(file=target_file)

            # Then we could hit multiple trunks.
            target_file = dir / "_trunk.node.md"
            if target_file.exists():
                level = 1
                trunk_dirs.append(str(dir.relative_to(root_dir)))
                trunk_texts.append(A_GIS.File.read(file=target_file))

            # Go up.
            dir = dir.parent

        # Then we hit the root.
        level = 0
        root_text = A_GIS.File.read(file=root_dir / "_root.node.md")
        root_reldir = "."

        # Assemble the context.
        heading = "#"
        context = f"{heading} STACKS root: {root_reldir}\n\n"
        context += root_text.strip() + "\n\n"
        if len(trunk_dirs) > 0:
            trunk_texts.reverse()
            trunk_dirs.reverse()
            trunk_dir = trunk_dirs[-1]
            trunk_text = "\n\n".join([t.strip() for t in trunk_texts])
            heading += "#"
            context += f"{heading} STACKS trunk: {trunk_dir}\n\n"
            context += trunk_text + "\n\n"
            if branch_dir:
                heading += "#"
                context += f"{heading} STACKS branch: {branch_dir}\n\n"
                context += branch_text.strip() + "\n\n"
                if leaf_dir:
                    heading += "#"
                    context += f"{heading} STACKS leaf: {leaf_dir}\n\n"
                    context += leaf_text.strip() + "\n\n"

    except BaseException as e:
        error = str(e)

    return A_GIS.Code.make_struct(
        error=error,
        root_text=root_text,
        root_reldir=root_reldir,
        branch_text=branch_text,
        branch_dir=branch_dir,
        trunk_texts=trunk_texts,
        trunk_text=trunk_text,
        trunk_dirs=trunk_dirs,
        trunk_dir=trunk_dir,
        leaf_text=leaf_text,
        leaf_dir=leaf_dir,
        context=context,
        dirname=str(dirname),
        _root_dir=str(root_dir),
        _target_dir=str(target_dir),
    )
