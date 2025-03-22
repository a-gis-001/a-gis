def show_tree(
    directory: str,
    max_levels: int = 2,
    num_per_dir: int = 10,
    only_extensions: list = None,
    indent_chars: int = 4,
    ignore_dot_files: bool = True,
    ignore_dirs=[],
    root_dir: str = None,
):
    """Show a directory's contents as a hierarchical tree.

    This function generates a text representation of the file system
    starting from a specified directory and recursively traversing
    subdirectories up to a maximum number of levels, with optional
    filters for file extensions and directories to ignore. It returns a
    structured string that includes counts of files by extension and a
    summary of shown versus total files and subdirectories.

    Args:
        directory (str):
            The path to the root directory to be displayed.
        max_levels (int):
            The maximum number of levels deep to traverse into
            subdirectories. Default is 2.
        num_per_dir (int):
            The maximum number of files or subdirectories to show for
            each directory level. Default is 10.
        only_extensions (list):
            A list of file extensions to include when displaying files.
            If None, all file extensions will be displayed. Default is
            None.
        indent_chars (int):
            The number of spaces to use for indentation at each level.
            Default is 4.
        ignore_dot_files (bool):
            Whether to exclude hidden files (those starting with a dot).
            Default is True.
        ignore_dirs (list):
            A list of directory names to ignore. Any directory
            containing all of the specified names will be skipped.
            Default is an empty list.
        root_dir (str):
            The root directory from which to calculate the relative
            paths of subdirectories. If not provided, the current
            directory is used as the root. Default is None.

    Returns:
        dataclass:
            With the following attributes

            - tree (str): A string representing the directory tree
              structure with optional counts and suppressed
              information.
            - path (str): The path to the root directory that was
              displayed in the tree.
    """

    import pathlib
    import A_GIS.Code.make_struct

    directory = pathlib.Path(directory)
    if root_dir and directory.relative_to(root_dir):
        top_dir = directory.relative_to(root_dir)
    else:
        top_dir = directory
    if not root_dir:
        root_dir = directory

    def _show_tree(dir_path: pathlib.Path, level: int) -> str:
        """Recursively builds the directory tree string."""
        indent = " " * indent_chars * level
        tree_str = ""

        items = sorted(dir_path.iterdir(), key=lambda x: x.name)
        if ignore_dot_files:
            items = [item for item in items if not item.name.startswith(".")]

        files = [item for item in items if item.is_file()]
        dirs0 = [item for item in items if item.is_dir()]

        # Filter directories.
        def keep(dir0, ignore_dirs):
            for i in ignore_dirs:
                if i in dir0.parts:
                    return False
            return True

        dirs = []
        for dir0 in dirs0:
            if keep(dir0, ignore_dirs):
                dirs.append(dir0)

        total_counts = {}
        for item in files:
            ext = item.suffix[1:] if item.suffix else ""
            total_counts[ext] = total_counts.get(ext, 0) + 1

        total_subdirs = len(dirs)
        shown_subdirs = 0

        # Show files if within max_levels
        shown_counts = {}
        shown_files = 0
        if level <= max_levels:
            for item in files:
                ext = item.suffix[1:] if item.suffix else ""
                if ext not in shown_counts:
                    shown_counts[ext] = 0
                if only_extensions is None or ext in only_extensions:
                    if shown_files < num_per_dir:
                        tree_str += indent + f"{item.relative_to(root_dir)}\n"
                        shown_files += 1
                        shown_counts[ext] += 1
        else:
            # Collect counts without displaying files
            for item in files:
                ext = item.suffix[1:] if item.suffix else ""
                if ext not in shown_counts:
                    shown_counts[ext] = 0

        # Show subdirectories if within max_levels
        if level < max_levels:
            for idx, item in enumerate(dirs):
                if idx < num_per_dir:
                    tree_str += indent + f"{item.relative_to(root_dir)}\n"
                    shown_subdirs += 1
                    tree_str += _show_tree(item, level + 1)
        else:
            # Collect counts without displaying subdirectories
            pass

        subdir_counts = {"shown": shown_subdirs, "total": total_subdirs}

        # Add suppressed information
        tree_str = (
            _add_suppressed_info(
                shown_counts, total_counts, subdir_counts, level
            )
            + tree_str
        )

        return tree_str

    def _add_suppressed_info(
        shown_counts: dict,
        total_counts: dict,
        subdir_counts: dict,
        level: int,
    ) -> str:
        """Adds information about suppressed entries to the tree string."""
        indent = " " * indent_chars * level
        files_shown = sum(shown_counts.values())
        total_files = sum(total_counts.values())

        if total_files > 0:
            shown_info = ", ".join(
                f"{shown_counts.get(ext,
                                    0)}/{total_counts[ext]} {ext.upper() if ext else 'NO EXT'}"
                for ext in sorted(total_counts)
            )
            files_info = f"### showing {files_shown}/{total_files} files with {shown_info}"
        else:
            files_info = "### showing 0/0 files"

        subdir_info = f"### showing {
            subdir_counts['shown']}/{
            subdir_counts['total']} subdirs"
        return indent + files_info + "\n" + indent + subdir_info + "\n"

    if not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory")

    return A_GIS.Code.make_struct(
        tree=str(top_dir) + "\n" + _show_tree(directory, 1)
    )
