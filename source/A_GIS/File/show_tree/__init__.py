def show_tree(
    directory: type["pathlib.Path"],
    max_levels: int,
    num_per_dir: int,
    only_extensions: list = None,
):
    """
    Generates a directory tree.

    Args:
        directory (pathlib.Path): The root directory to start the tree.
        max_levels (int): The recursive depth to show.
        num_per_dir (int): The maximum number of entries to show per directory.
        only_extensions (list, optional): List of file extensions to include in the tree.

    Returns:
        str: A string representation of the directory tree.
    """
    import pathlib

    def _show_tree(dir_path: pathlib.Path, level: int) -> str:
        """Recursively builds the directory tree string."""
        if level > max_levels:
            return ""

        tree_str = ""
        suppressed_counts = {ext: 0 for ext in (only_extensions or [])}
        total_counts = {ext: 0 for ext in (only_extensions or [])}

        for item in sorted(dir_path.iterdir()):
            if item.is_dir():
                tree_str += "  " * level + f"{item.name}/\n"
                tree_str += _show_tree(item, level + 1)
            elif item.is_file() and (
                only_extensions is None or item.suffix in only_extensions
            ):
                total_counts[item.suffix] += 1
                if total_counts[item.suffix] <= num_per_dir:
                    tree_str += "  " * level + f"{item.name}\n"
                else:
                    suppressed_counts[item.suffix] += 1

        tree_str += _add_suppressed_info(
            suppressed_counts, total_counts, level, num_per_dir
        )
        return tree_str

    def _add_suppressed_info(
        suppressed_counts: dict,
        total_counts: dict,
        level: int,
        num_per_dir: int,
    ) -> str:
        """Adds information about suppressed entries to the tree string."""
        if any(count > 0 for count in suppressed_counts.values()):
            suppressed_info = ", ".join(
                f"{count}/{total_counts[ext]} {ext[1:].upper()}"
                for ext, count in suppressed_counts.items()
                if count > 0
            )
            return (
                "  " * level
                + f"... {sum(suppressed_counts.values())} entries suppressed exceeding num_per_dir={num_per_dir}\n"
                + "  " * level
                + suppressed_info
                + "\n"
            )
        return ""

    if not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory")

    return _show_tree(directory, 0)
