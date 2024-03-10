def get_console_width(*, max_width: int = 80):
    """Get the console width with a maximum limit"""
    import rich

    # Choose the smaller of the current width or the specified maximum width
    current_width = rich.console.Console().width
    return min(current_width, max_width)
