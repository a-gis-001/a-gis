def generate_summary(*, directory: type["path.Pathlib"], max_iterations=10):
    """Generates a summary of the directory contents."""
    import A_GIS.Ai.Chatbot.init
    import os
    import pathlib
    import A_GIS.File.read_to_text
    import A_GIS.File.show_tree

    def handle_requests(chatbot, response_content):
        import re

        request_block = re.search(
            r"<requests>(.*?)</requests>", response_content, re.DOTALL
        )
        if not request_block:
            return ""

        requests = request_block.group(1).strip().split("\n")
        if len(requests) > 1:
            return "Error: More than one request found."

        request = requests[0]
        if request.startswith("SHOW_TREE"):
            _, directory, nlevels, nperdir, *extensions = request.split()
            nlevels = int(nlevels)
            nperdir = int(nperdir)
            extensions = extensions if extensions else None
            result = A_GIS.File.show_tree(
                directory=pathlib.Path(directory),
                levels=nlevels,
                num_per_dir=nperdir,
                only_extensions=extensions,
            )
        elif request.startswith("READ_FILE"):
            _, file, beginchar, endchar = request.split()
            beginchar = int(beginchar)
            endchar = int(endchar)
            with open(file, "r") as f:
                f.seek(beginchar)
                result = f.read(endchar - beginchar)
        else:
            result = "Error: Invalid request."

        return result

    system_prompt = f"""
    You are a summarization bot tasked with generating summaries of directory contents.
    You emit a new block called <requests> where you ask to use a single tool.
    The available tools are: SHOW_TREE and READ_FILE.

    1. SHOW_TREE directory nlevels nperdir ext1 ext2 ...
    2. READ_FILE file beginchar endchar

    SHOW_TREE takes a directory path, the recursive depth (nlevesl), the number of files
    per directory (nperdir), and a list of file extensions to show. Any other files
    are suppressed.

    READ_FILE takes a file path and the beginning character index (beginchar) and
    the ending character index (endchar) and returns the text between those characters.
    If the file is not convertible to text you will see binary garbage.

    Your <output> block will always contain your best attempt at a summary.
    If you do not have a <requests> block, we'll assume you are finished and take
    whatever is in the <output> block as the final summary.

    Your summary should be in Markdown format, but a simple single paragraph without
    title or headings.

    The current settings allow {max_iterations} back and forth iterations to
    arrive at the final summary.
    """
    chatbot = A_GIS.Ai.Chatbot.init(model="reflection", system=system_prompt)

    summary_file_path = directory / "_summary.md"
    existing_summary = ""
    if summary_file_path.exists():
        existing_summary = A_GIS.File.read_to_text(path=summary_file_path)

    # Generate a directory tree that is at most 2 levels deep and only shows the following files.
    # .py, .pdf, .docx, .md,
    contents = A_GIS.File.show_tree(
        directory=directory,
        levels=2,
        only_extensions=["pdf", "py", "docx", "md"],
    )

    message = f"Current summary:\n{existing_summary}\n\nDirectory contents:\n{contents}\n\nPlease summarize the contents."

    for iteration in range(max_iterations):
        result = chatbot.chat(message, keep_state=True)
        requests = handle_requests(chatbot, result["message"]["content"])
        if requests == "":
            # No more requests mean the final summary has been made.
            break
        else:
            # If there are requests, then we update the prompt.
            message = f"Iteration {iteration+1}/{max_iterations}. Here are the replies to your requests:\n\n{requests}"

    return extract_summary(result)
