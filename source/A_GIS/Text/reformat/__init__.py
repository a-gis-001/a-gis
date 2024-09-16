def reformat(
    *,
    text: str,
    width: int = 72,
    indent: int = 0,
    collapse_whitespace: bool = True,
):
    """Format text to wrap within a specified width.

    Maintains paragraph integrity and original indentation, with optional
    whitespace reduction after wrapping.

    Args:
        text (str): The source text to be reformatted.
        width (int, optional): The maximum number of characters per line.
            Defaults to 72.
        indent (int, optional): Indent reformatted text.
        collapse_whitespace (bool, optional): If True, collapses whitespace
            between words to a single space after wrapping. Defaults to True.

    Returns:
        str: A new string containing the text with lines wrapped to fit within
        the specified width, preserving paragraph breaks and original indentation.
    """
    import re
    import textwrap
    import A_GIS.Text.insert_block_placeholders
    import A_GIS.Text.reconstitute_blocks

    # Step 1: Remove extra newlines, but preserve paragraph breaks.
    text = re.sub(r"\n\n+", r"\n\n", text)
    text = text.rstrip()

    # Step 2: Insert placeholders for blocks (e.g., code or special text) that
    # should not be wrapped.
    subs, text = A_GIS.Text.insert_block_placeholders(
        text=text, block_name=r"\S*"
    )

    # Step 2: Split text into lines, preserving line breaks.
    lines = text.splitlines(keepends=True)

    # Define a regex to detect list markers (e.g., '-', '*', or numbered lists)
    list_marker_pattern = re.compile(r"^(\s*(?:[-*]|\d+\.)\s+)")

    wrapped_text = ""
    paragraph = ""

    for line in lines:
        if line.strip() == "":
            # Empty line indicates paragraph break
            if paragraph:
                # Wrap the accumulated paragraph
                wrapped_paragraph = textwrap.fill(
                    paragraph.strip(),
                    width=width - indent,
                    replace_whitespace=collapse_whitespace,
                    break_long_words=False,
                    initial_indent=" " * indent,
                    subsequent_indent=" " * indent,
                )
                wrapped_text += wrapped_paragraph + "\n\n"
                paragraph = ""
            else:
                # Preserve multiple empty lines
                wrapped_text += "\n"
        elif list_marker_pattern.match(line):
            # Line is a list item
            if paragraph:
                # Wrap the previous paragraph before handling the list item
                wrapped_paragraph = textwrap.fill(
                    paragraph.strip(),
                    width=width - indent,
                    replace_whitespace=collapse_whitespace,
                    break_long_words=False,
                    initial_indent=" " * indent,
                    subsequent_indent=" " * indent,
                )
                wrapped_text += wrapped_paragraph + "\n\n"
                paragraph = ""

            # Extract the list marker and content
            list_marker = list_marker_pattern.match(line).group(1)
            content = line[len(list_marker) :].strip()

            # Wrap the list item with proper indentation
            wrapped_item = textwrap.fill(
                content,
                width=width - indent - len(list_marker),
                replace_whitespace=collapse_whitespace,
                break_long_words=False,
                initial_indent=" " * indent + list_marker,
                subsequent_indent=" " * (indent + len(list_marker)),
            )
            wrapped_text += wrapped_item + "\n"
        else:
            # Accumulate lines for the current paragraph
            paragraph += line

    # Wrap any remaining text in the paragraph buffer
    if paragraph:
        wrapped_paragraph = textwrap.fill(
            paragraph.strip(),
            width=width - indent,
            replace_whitespace=collapse_whitespace,
            break_long_words=False,
            initial_indent=" " * indent,
            subsequent_indent=" " * indent,
        )
        wrapped_text += wrapped_paragraph + "\n"

    # Clean up extra newlines and trailing whitespace
    wrapped_text = re.sub(r"\n{3,}", "\n\n", wrapped_text).rstrip("\n")

    # Step 5: Reinsert the code blocks into their original positions
    reformatted_text = A_GIS.Text.reconstitute_blocks(
        text=wrapped_text, subs=subs
    )

    return reformatted_text
