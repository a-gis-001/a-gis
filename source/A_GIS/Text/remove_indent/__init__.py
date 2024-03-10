def remove_indent(*, text: str):
    """Remove leading whitespace indentation from a block of text

    This function takes a multi-line string as input and removes any common leading whitespace
    from each line of the text, effectively de-indenting it. It will skip empty lines but
    as soon as a line with less indentation is found, it will return.

    Args:
        text (str): A multiline string to be de-indented.

    Returns:
        str: The input string, but with any common leading whitespace removed from each line.
    """

    import A_GIS.Text.get_indent

    # Find the indentation of the first line
    lines = text.splitlines()
    min_indent = A_GIS.Text.get_indent(lines[0])

    # Deindent lines, stop on the first line that would be truncated and return the
    # potentially shorter string.
    deindented_lines = []
    for line in lines:
        if not line.strip():  # Keep empty lines
            deindented_lines.append(line)
        elif get_indent(line) >= min_indent:
            deindented_lines.append(line[min_indent:])
        else:
            break

    # Reconstruct the text
    return "\n".join(deindented_lines)
