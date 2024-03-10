def get_git_status(*, root: str):
    """Get the git status of a specified directory.

    This function runs a 'git status' command for a given root directory and returns
    the result as a styled rich Text object within a Panel. The output is also formatted to remove tabs.

    Args:
        root (str): The root directory where the git status should be checked.

    Raises:
        None

    Returns:
        rich.panel.Panel: A styled panel containing the git status output for the specified directory.
    """

    import subprocess
    import rich

    command = ["git", "-c", "color.ui=always", "status", f"{root}"]
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Get the command output
    command_output = completed_process.stdout
    lines = command_output.splitlines()
    stripped_lines = [line.rstrip() for line in lines]
    command_output = "\n".join(stripped_lines)

    command_output = command_output.replace("\t", "    ")
    # Create a Text object with the command output for styling
    output_text = rich.text.Text.from_ansi(command_output)
    panel = rich.panel.Panel(
        output_text,
        title=f"git status {root}",
        expand=True,
        border_style="bold cyan",
    )

    return panel
