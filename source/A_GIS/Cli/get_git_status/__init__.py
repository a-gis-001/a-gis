def get_git_status(*, root: str):
    """Return the git status of a specified directory.

    This function uses the `run_git` utility to execute the 'git status'
    command on the provided root directory. It returns the output of the
    command, which includes information about the current state of the
    repository, such as modified files and untracked files.

    Args:
        root (str):
            The path to the git repository for which the status is
            requested.

    Returns:
        str:
            The output from the 'git status' command executed on the
            specified directory.
    """

    import A_GIS.Cli.run_git

    return A_GIS.Cli.run_git(
        mode="status", args=[str(root)], return_panel=True
    ).panel
