def get_leaf(*, path: type["pathlib.Path"]):
    """Get the leaf node directory."""
    current_path = path
    while True:
        # Check for _summary.md file
        if (current_path / "_summary.md").exists():
            return current_path

        # Check for _scope.md file
        if (current_path / "_scope.md").exists():
            return None

        # Check for _inbox directory
        if (current_path / "_inbox").is_dir():
            return None

        # Move up one directory
        parent_path = current_path.parent
        if parent_path == current_path:  # Reached the root
            return None
        current_path = parent_path
