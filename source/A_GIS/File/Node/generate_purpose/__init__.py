def generate_purpose(
    *,
    directory: type["path.Pathlib"],
    max_iterations=10,
    root_dir=None,
    overwrite_existing: bool = False,
):
    """Generate a concise purpose statement for content in a directory.

    This function generates a purpose statement that declares purpose and
    contents of a given directory, based on the directory's structure and
    the contents of files like `_purpose.md`. It uses an AI chatbot to parse
    requests for showing directory tree structures or reading specific parts
    of files within the directory. The function iteratively communicates
    with the chatbot until a final summary is reached, up to a specified
    maximum number of iterations.

    Args:
        directory (type:
            pathlib.Path): The path to the target directory for which the summary
            should be generated.
        max_iterations (int, optional):
            The maximum number of iterations allowed for the chatbot to reach a
            final summary. Defaults to 10.
        root_dir (pathlib.Path, optional):
            The root directory from which relative paths are calculated for the AI
            chatbot's requests. If None, the `directory` itself is used as the root
            directory.
        overwrite_existing (bool, optional):
            A flag indicating whether to overwrite the existing `_purpose.md` file
            in the target directory. Defaults to False.

    Returns:
        str:
            A Markdown formatted purpose for the directory.
    """
    import A_GIS.Ai.Chatbot.init
    import os
    import pathlib
    import A_GIS.File.read_to_text
    import A_GIS.File.show_tree
    import A_GIS.File.is_subdirectory

    if not root_dir:
        root_dir = directory

    def parse_request(request):
        if request.startswith("SHOW_TREE"):
            _, subdir, nlevels, nperdir, *extensions = request.split()
            nlevels = int(nlevels)
            nperdir = int(nperdir)
            extensions = extensions if extensions else None
            abs_subdir = root_dir / subdir
            if not abs_subdir.exists():
                result = f"The requested directory {subdir} does not exist."
            elif not A_GIS.File.is_subdirectory(
                parent=root_dir, sub=abs_subdir, allow_same=True
            ):
                result = f"The requested directory {subdir} is not a subdirectory (.. not allowed)."
            else:
                result = A_GIS.File.show_tree(
                    directory=abs_subdir,
                    max_levels=nlevels,
                    num_per_dir=nperdir,
                    only_extensions=extensions,
                    root_dir=root_dir,
                )
        elif request.startswith("READ_FILE"):
            _, file, beginchar, endchar = request.split()
            abs_file = root_dir / file
            if not abs_file.exists():
                result = f"The requested file {file} does not exist."
            elif not A_GIS.File.is_subdirectory(
                parent=root_dir, sub=abs_file, allow_same=True
            ):
                result = f"The requested file {file} is not in a subdirectory (.. not allowed)."
            text = A_GIS.File.read_to_text(file=abs_file)
            beginchar = min(max(0, int(beginchar)), len(text) - 1)
            endchar = min(max(0, int(endchar)), len(text) - 1)
            if endchar > beginchar:
                result = text[beginchar:endchar]
            else:
                result = f"Error: requested beginchar {beginchar} and endchar {endchar} do not make sense."
        else:
            result = f"Error: Invalid request {request} should start with SHOW_TREE or READ_FILE."

        return result

    def handle_requests(chatbot, response_content):
        import re

        request_block = re.search(
            r"<request>(.*?)</request>", response_content, re.DOTALL
        )
        if not request_block:
            return ""

        requests = request_block.group(1).strip().split("\n")
        if len(requests) > 1:
            return "Error: More than one request found."

        return parse_request(requests[0])

    def extract_purpose(response_content):
        import re

        block = re.search(
            r"<output>(.*?)</output>", response_content, re.DOTALL
        )
        if not block:
            return ""
        else:
            return block.group(1).strip()

    reminder = """
    Remember, your <output> block must always contain your best guess for the purpose.
    If you do not put a <request> block in your message, we'll assume you are finished
    and take whatever is in the <output> block as the final purpose statement.
    """
    system_prompt = f"""
    You are a interpretation AI tasked with generating the purpose of a directory
    in a file system based on any files currently in that directory. This purpose
    is stored in a special file called `_purpose.md`.

    You have tools at your disposal which you call using a <request> block.

    1. SHOW_TREE directory nlevels nperdir ext1 ext2 ...
    2. READ_FILE file beginchar endchar

    SHOW_TREE takes a directory path, the recursive depth (nlevels), the number of files
    per directory (nperdir), and a list of file extensions to show. Any other files
    are suppressed.

    READ_FILE takes a file path and the beginning character index (beginchar) and
    the ending character index (endchar) and returns the text between those characters.
    READ_FILE supports reading many file formats like DOCX and PDF. If the file is not
    internally convertible to a text representation, you will see binary garbage.

    Your purpose should be short, concise, and in Markdown format.

    The current settings allow {max_iterations} back and forth iterations to
    arrive at the final summary.

    An example of a request is:
    <request>
    SHOW_TREE my_dir/test/_ 2 10 py
    </request>
    Which would should the directory my_dir/test/_, with 2 levels of recursion,
    a maximum of 10 files, and only for .py extensions.

    A follow-up request could be:
    <request>
    READ_FILE my_dir/test/_/plot.py 0 999
    </request>
    Which would show the first 1000 characters in the file, my_dir/test/_/plot.py.

    When you reference files within the directory, use their relative paths. For
    example, instead of putting "`xyz.py` in directory `uvw`", put
    "file `uvw/xyz.py`".

    Do not refer to the `_purpose.md` file in your <output> description. You can use
    its contents as a way to help you understand the previous thoughts on the purpose
    of the directory, but your main job is to update the `_purpose.md` file with an
    updated purpose statement.

    Do not refer to the '.' directory. Your purpose statement should have a H2 heading,
    and state directly the purpose, followed by another H2 heading for a list of key
    contents. For example.

    ## Purpose

    To store documents related to William Wieselquist's professional
    profile, career development, and research activities.

    ## Key Contents

    - `waw_cv-2024.docx`: latest CV
    - `waw_cv-2024.pdf`: PDF version of his CV
    - `works.bib`: bibliography file of research publications

    Be concise like the example! Instead of "contains his latest CV with work experience"
    just say "latest CV". Because the context is already describing "Key Contents",
    you don't need to repeat "contains" or other similar words. Also a CV contains
    work experience and leadership roles by definition, so "CV" suffices. These are
    just examples. Use this type of judgement in all your statements.

    This file structure has a convention to support an optional directory `_` that can
    contain related files/subdirs. These may be simple symlinks. You should generally
    treat content that is within a `_` directory as less important in defining the
    purpose than other content outside the `_` directory.

    Use your <thinking> block to interpret the result of your last request, relate it
    to the overarching goal to determine the purpose for this directory, and then
    plan your next actions.

{reminder}
    """

    chatbot = A_GIS.Ai.Chatbot.init(
        model="reflection",
        system=system_prompt,
        num_predict=15000,
        num_ctx=30000,
        temperature=0.7,
    )

    purpose_file_path = (directory / "_purpose.md").resolve()

    existing_purpose = "FILE DOES NOT EXIST"
    if purpose_file_path.exists():
        existing_purpose = A_GIS.File.read_to_text(file=purpose_file_path)
    top_dir = directory.relative_to(root_dir)

    request = f"SHOW_TREE {str(top_dir)} 2 10"
    contents = parse_request(request)
    message = f"""
Current purpose statement '{str(top_dir)}/_purpose.md':
{existing_purpose}

Initial SHOW_TREE request:
<request>
{request}
</request>

Contents:
{contents}

Please assign a purpose to the '{str(top_dir)}' directory.
    """

    for iteration in range(max_iterations):
        result = chatbot.chat(message, keep_state=True)
        requests = handle_requests(chatbot, result["message"]["content"])
        if requests == "":
            # No more requests mean the final purpose has been declared.
            break
        else:
            # If there are requests, then we update the prompt.
            message = f"Iteration {iteration+1}/{max_iterations}. Here are the replies to your requests:\n\n{requests}\n\n{reminder}"

    # Extract the final purpose statement and reformat to be pretty.
    purpose = extract_purpose(result["message"]["content"])
    purpose = A_GIS.Text.reformat(text=purpose)

    # Overwrite the existing file.
    if overwrite_existing:
        A_GIS.File.write(file=directory / "_purpose.md", content=purpose)

    return purpose
