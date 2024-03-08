def is_function(*, code: str):
    import re

    # Matches `def` at the start of a line, with no leading whitespace
    return bool(re.search(r"^def ", code, flags=re.MULTILINE)) and not bool(
        re.search(r"^class ", code, flags=re.MULTILINE)
    )
