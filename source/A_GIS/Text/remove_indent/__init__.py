def remove_indent(text):
    lines = text.splitlines()
    # Find the indentation of the first line
    min_indent = get_indent(lines[0])

    # Deindent lines, skip lines that would be truncated
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
