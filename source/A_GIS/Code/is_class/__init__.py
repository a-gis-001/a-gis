def is_class(*, code: str):
    # Matches `class` at the start of a line, with no leading whitespace
    import re

    return bool(re.search(r"^class ", code, flags=re.MULTILINE)) and not bool(
        re.search(r"^def ", code, flags=re.MULTILINE)
    )
