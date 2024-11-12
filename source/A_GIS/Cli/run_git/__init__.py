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
        mode (str):
            The Git subcommand to execute (e.g., "status", "log").
        args (list[str]):
            A list of additional arguments to pass to the Git command
            along with `mode`.
        return_panel (bool, optional):
            If True, the function will return a rich UI panel displaying
            the Git output. The panel includes styled text and a title
            based on the executed command. Defaults to False.

    Returns:
        A_GIS.Code.make_struct:
            With the following attributes

            - panel (rich.panel.Panel, optional):
            A rich UI panel displaying the Git output if `return_panel`
            is True.

            - output (str):
            The plain text output from the executed Git command.

            - stderr (str):
            Any standard error output from the executed Git command.

            - _mode (str):
            The mode of the Git command that was executed.

            - _args (list[str]):
            The arguments passed to the Git command.
    """

    import subprocess
    import A_GIS.Code.make_struct

    command = ["git"]
    if return_panel:
        command.extend(["-c", "color.ui=always"])
    command.extend([mode, *args])

    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Get the command output
    command_output = completed_process.stdout
    lines = command_output.splitlines()
    stripped_lines = [line.rstrip() for line in lines]
    command_output = "\n".join(stripped_lines)

    command_output = command_output.replace("\t", "    ")

    panel = None
    if return_panel:
        import rich

        # Create a Text object with the command output for styling
        output_text = rich.text.Text.from_ansi(command_output)
        args_str = " ".join(args)
        panel = rich.panel.Panel(
            output_text,
            title=f"git {mode} {args_str}",
            expand=True,
            border_style="bold cyan",
        )

    return A_GIS.Code.make_struct(
        panel=panel,
        output=command_output,
        stderr=completed_process.stderr,
        _mode=mode,
        _args=args,
    )
