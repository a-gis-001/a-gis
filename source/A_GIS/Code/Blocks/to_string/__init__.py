def to_string(*, blocks=[], start_index=0):
    """Convert blocks to a string."""

    s = "+--+" + "-" * 80 + "+\n"
    for b in blocks:
        for l in b:
            s += "|{:02d}|{:80s}|\n".format(start_index, l)
        s += "+--+" + "-" * 80 + "+\n"
        start_index += 1

    return s
