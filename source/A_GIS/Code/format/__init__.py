def format(code: str) -> str:
    import autopep8
    import black
    import re

    # Format with autopep8.
    formatted_code = autopep8.fix_code(
        code, options={"aggressive": True, "aggressive": True}
    )

    # Format with black.
    BLACK_MODE = black.Mode(
        target_versions={black.TargetVersion.PY311}, line_length=79
    )
    try:
        formatted_code = black.format_file_contents(
            formatted_code, fast=False, mode=BLACK_MODE
        )
    except black.NothingChanged:
        pass
    finally:
        # Make sure there's a newline after the content
        if formatted_code and formatted_code[-1] != "\n":
            formatted_code += "\n"

    # Remove multiple new lines.
    formatted_code = re.sub(r"\n\s*\n", "\n\n", formatted_code)

    # Remove tabs.
    formatted_code = formatted_code.expandtabs(4)

    # Return formatted code.
    return formatted_code
