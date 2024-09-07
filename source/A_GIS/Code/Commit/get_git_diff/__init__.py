def get_git_diff(*, args:list):
    """Get the git diff in the current directory."""
    import subprocess

    command = ["git", "diff", *args]
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    return completed_process.stdout
