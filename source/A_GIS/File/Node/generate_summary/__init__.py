def generate_summary(
    *,
    directory: type["path.Pathlib"],
    max_iterations=10,
    root_dir=None,
    overwrite_existing: bool = False,
):
    """Generate concise Markdown directory summary using AI chatbot interactions.

    This function generates a summary that describes the purpose and
    contents of a given directory, based on the directory's structure and
    the contents of files like `_summary.md`. It uses an AI chatbot to parse
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
            A flag indicating whether to overwrite the existing `_summary.md` file
            in the target directory. Defaults to False.

    Returns:
        str:
            A Markdown formatted summary of the directory's contents. The summary includes a description
            of the directory's purpose, a structured outline of its contents derived from the `SHOW_TREE` requests,
            and text extracts from files within the directory as per the `READ_FILE` requests.
    """
    import A_GIS.Ai.Chatbot.init
    import os
    import pathlib
    import A_GIS.File.read_to_text
    import A_GIS.File.show_tree

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

    def extract_summary(response_content):
        import re

        block = re.search(
            r"<output>(.*?)</output>", response_content, re.DOTALL
        )
        if not block:
            return ""
        else:
            return block.group(1).strip()

    reminder = """
    Remember, your <output> block will always contain your best attempt at a summary.
    If you do not put a <request> block in your message, we'll assume you are finished
    and take whatever is in the <output> block as the final summary.
    """
    system_prompt = f"""
    You are a summarization bot tasked with generating a new or updated _summary.md file
    which describes why a directory exists. What is it's purpose?

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

    Your summary should be a short, concise description in Markdown format.

    The current settings allow {max_iterations} back and forth iterations to
    arrive at the final summary.

    An example of a request is:
    <request>
    SHOW_TREE my_dir/test/_ 2 10 py
    </request>
    Which would should the directory my_dir/test/_, with 2 levels of recursion, a maximum of 10 files, and only for .py extensions.

    A follow-up request could be:
    <request>
    READ_FILE my_dir/test/_/plot.py 0 999
    </request>
    Which would show the first 1000 characters in the file, my_dir/test/_/plot.py.

    As you are writing the final summary, format it nicely with paragraphs, lists, etc.
    from Markdown and don't make lines too long (80 characters wide is a good limit).

    When you reference files within the directory, try to use their relative paths so that
    the Markdown can link to them easily. I.e. instead of saying file `xyz.py` in directory
    `uvw`, say file `uvw/xyz.py`. Never refer to the '.' directory. Just refer to this
    directory, i.e. "This directory contains ...".

    Do not refer to the _summary.md file in your description (this is the file you
    are updating).

    The convention for this structure is that a directory called `_` can contain
    additional subdirectories that may be symlinked and should not be altered
    by this organization system. Files that are not within a _ directory may be
    moved around by another bot when they are found to better match another directory.

    Part of this matching is based on the content of _summary.md, so it should help
    other bots choose good additional content for this directory.

    Place all your thoughts in your normal <thinking> block. In your <output> block
    always present your best attempt at a confident, full description that will be
    refined as you learn more.

{reminder}
    """

    chatbot = A_GIS.Ai.Chatbot.init(
        model="reflection",
        system=system_prompt,
        num_predict=15000,
        num_ctx=30000,
        temperature=0.7,
    )

    summary_file_path = directory / "_summary.md"
    existing_summary = "FILE DOES NOT EXIST"
    if summary_file_path.exists():
        existing_summary = A_GIS.File.read_to_text(file=summary_file_path)

    top_dir = directory.relative_to(root_dir)

    request = f"SHOW_TREE {str(top_dir)} 2 10"
    contents = parse_request(request)
    message = f"""
Current summary '{str(top_dir)}/_summary.md':
{existing_summary}

Initial SHOW_TREE request:
<request>
{request}
</request>

Contents:
{contents}

Please summarize the contents of the '{str(top_dir)}' directory.
    """

    for iteration in range(max_iterations):
        result = chatbot.chat(message, keep_state=True)
        requests = handle_requests(chatbot, result["message"]["content"])
        if requests == "":
            # No more requests mean the final summary has been made.
            break
        else:
            # If there are requests, then we update the prompt.
            message = f"Iteration {iteration+1}/{max_iterations}. Here are the replies to your requests:\n\n{requests}\n\n{reminder}"

    # Extract the final summary and reformat to be pretty.
    summary = extract_summary(result["message"]["content"])
    summary = A_GIS.Text.reformat(text=summary)

    # Overwrite the existing file.
    if overwrite_existing:
        A_GIS.File.write(file=directory / "_summary.md", text=summary)

    return summary
