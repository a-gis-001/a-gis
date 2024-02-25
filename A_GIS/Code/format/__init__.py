def format(code: str) -> str:
    # Format with autopep8.
    import autopep8

    formatted_code = autopep8.fix_code(
        code, options={"aggressive": True, "aggressive": True}
    )

    # Format with docformatter.
    from docformatter import __main__ as main
    import io

    stdout = io.StringIO()
    stdin = io.StringIO(formatted_code)
    main._main(
        argv=["/path/to/docformatter", "--force-wrap", "-"],
        standard_out=stdout,
        standard_error=None,
        standard_in=stdin,
    )
    formatted_code = stdout.getvalue()

    # Format with black.
    import black

    BLACK_MODE = black.Mode(target_versions={black.TargetVersion.PY311}, line_length=79)
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
    import re

    formatted_code = re.sub(r"\n\s*\n", "\n\n", formatted_code)

    return formatted_code
