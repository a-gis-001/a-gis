def get_git_diff(*, diff_args:list=["--staged"]):

    command = ["git", *list]
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Get the command output
    return completed_process.stdout
