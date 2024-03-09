def add_indent(text, spaces=4):
    import re

    return re.sub(r"^", " " * spaces, text, flags=re.MULTILINE)
