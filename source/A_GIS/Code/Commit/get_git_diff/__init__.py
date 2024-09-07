def get_git_diff(*, args: list):
    """Get the git diff in the current directory.

    Execute a 'git diff' command with the given arguments and returns the resulting diff as plain text, utilizing the `subprocess` module to run the command.
    returns the output of the diff as plain text. It utilizes the `subprocess` module to
    run the git command.

    Args:
        args (List[str]):
            A list of arguments to be passed to the 'git diff' command.
            Typically, this would include file paths or other options relevant to the
            diff you want to obtain.

    Returns:
        str:
            A string containing the diff output.

    Raises:
        subprocess.CalledProcessError:
            If the git command fails, a CalledProcessError
            exception with the returncode of the command is raised.
        FileNotFoundError:
            If 'git' is not available in the system's PATH, a
            FileNotFoundError exception is raised.
    """

    import subprocess

    command = ["git", "diff", *args]
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    return completed_process.stdout
