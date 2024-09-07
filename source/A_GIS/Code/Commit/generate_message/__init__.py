def generate_message(*, do_commit=False, diff_args: list=["--staged"], **kwargs):

    import A_GIS.Code.Commit.get_git_diff
    import A_GIS.Ai.Chatbot.init
    import textwrap

    coder = A_GIS.Ai.Chatbot.init(
        model="reflection",
        system="""
        You look at the output of a git diff and recommend a commit message.
        Follow the 50/72 rule for commit messages.

        * The first line should be a short summary (50 characters or less with no quotes)
          that describes the change.
        * The second line should be blank.
        * The third line and onwards can contain a longer description of the change but
          should not repeat any information from the first line.

        Please wrap all lines to 72 characters and indent appropriately for a commit
        message that is easy to read.

        Only include the commit message between your output tags:
        <output> commit message </output>.

        For example,

        <output>
        Add Commit package and refactor code generation

        Added a new package called `Commit` which contains functions for
        generating commit messages. It also refactors the code generation
        process to use these new functions. Additionally, it updates various
        other packages and files to use the new `Commit` package.
        </output>

        """,
        **kwargs,
    )

    result = coder.chat(message=A_GIS.Code.Commit.get_git_diff(args=diff_args))
    content = result["message"]["content"]

    output = A_GIS.Text.get_between_tags(text=content,begin_tag='<output>',end_tag='</output>').strip()

    # Reformat into a proper 50/72
    lines = output.split("\n")
    first_sentence = lines[0]
    remaining_text = ''
    if len(lines)>1:
        remaining_text="\n".join(lines[1:])
    remaining_text = textwrap.fill(textwrap.dedent(remaining_text), width=72).strip()
    message = f"{first_sentence}\n\n{remaining_text}\n"
    if do_commit:
        import subprocess

        command = ["git", "commit", "-m", message]
        completed_process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

    return message


