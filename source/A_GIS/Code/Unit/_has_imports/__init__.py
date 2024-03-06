def _has_imports(*, block: list[str]) -> bool:
    """Check if the block contains import statements."""
    return any(
        line.lstrip().startswith(("from ", "import ")) for line in block
    )
