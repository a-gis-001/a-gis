def show_tree(
    directory: str,
    max_levels: int = 2,
    num_per_dir: int = 10,
    only_extensions: list = None,
    indent_chars: int = 4,
    ignore_dot_files: bool = True,
    root_dir: str = None,
):
    """Display the contents of a directory in a tree-like structure.

    This function generates a textual representation of a directory's
    contents, showing files and subdirectories up to a specified number
    of levels deep. It supports filtering by file extensions and can be
    configured to ignore dotfiles (hidden files starting with a dot).

    Args:
        directory (str):
            The path to the directory whose contents are to be
            displayed.
        max_levels (int):
            The maximum depth of directories to display. Default is 2.
        num_per_dir (int):
            The number of files and subdirectories to show for each
            level. Default is 10.
        only_extensions (list):
            A list of file extensions to filter the displayed files by.
            If None, all files are shown. Default is None.
        indent_chars (int):
            The number of spaces to indent subdirectories and files.
            Default is 4.
        ignore_dot_files (bool):
            Whether to exclude dotfiles from the display. Default is
            True.
        root_dir (str):
            The root directory relative to which the specified directory
            is displayed. If not provided, the specified directory
            becomes the root. Default is None.

    Returns:
        dataclass:
            With the following attributes

            - tree (str): A string representation of the directory
              tree structure.
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
        dirs = [item for item in items if item.is_dir()]

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
                f"{shown_counts.get(ext, 0)}/{total_counts[ext]} {ext.upper() if ext else 'NO EXT'}"
                for ext in sorted(total_counts)
            )
            files_info = f"### showing {files_shown}/{total_files} files with {shown_info}"
        else:
            files_info = "### showing 0/0 files"

        subdir_info = f"### showing {subdir_counts['shown']}/{subdir_counts['total']} subdirs"
        return indent + files_info + "\n" + indent + subdir_info + "\n"

    if not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory")

    return A_GIS.Code.make_struct(
        tree=str(top_dir) + "\n" + _show_tree(directory, 1)
    )
