def run_git(
    *, mode: str = "status", args: list[str], return_panel: bool = False
):
    """Run a Git command and return output with optional UI panel.

    This function runs a Git command specified by `mode` and `args`, and
    returns a structured result that may include a rich UI panel for
    displaying the output if `return_panel` is True. The command's
    output is returned as plain text, while any standard error output is
    also included in the return value.

    Args:
        mode (str, optional): The Git subcommand to execute (e.g., "status", "log").
            Defaults to "status"
        args (list[str]): A list of additional arguments to pass to the Git command
            along with `mode`
        return_panel (bool, optional): If True, the function will return a rich UI panel displaying
            the Git output. The panel includes styled text and a title
            based on the executed command. Defaults to False

    Returns:
        Result: A dataclass with the following attributes:
            - panel: A rich UI panel displaying the Git output if `return_panel`
              is True
            - output: The plain text output from the executed Git command
            - stderr: Any standard error output from the executed Git command
            - _mode: The mode of the Git command that was executed
            - _args: The arguments passed to the Git command
    """

    import subprocess
    import A_GIS.Code.make_struct

    # Assemble the git command.
    command = [
        "git",
        *(("-c", "color.ui=always") if return_panel else ()),
        mode,
        *args,
    ]

    # Run the command.
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Get a cleaned up version of the output.
    command_output = "\n".join(
        line.rstrip() for line in completed_process.stdout.splitlines()
    ).replace("\t", "    ")

    # Assemble the panel, if requested.
    panel = None
    if return_panel:
        import rich

        panel = rich.panel.Panel(
            rich.text.Text.from_ansi(command_output),
            title=f"git {mode} {' '.join(args)}",
            expand=True,
            border_style="bold cyan",
        )

    # Return the output.
    return A_GIS.Code.make_struct(
        panel=panel,
        output=command_output,
        stderr=completed_process.stderr,
        _mode=mode,
        _args=args,
    )
