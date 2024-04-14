def _check_body_block(*, block: list[str], start_index: int = 0) -> list[str]:
    """Checks a code block for compliance with comment and import rules.

    Specifically, this function ensures that the block starts with a
    comment, contains no internal comments after code has started, and does
    not include any import statements unless it's the first block. If any of
    these conditions are not met, appropriate error messages are generated.

    Args:
        block: A list of strings, each representing a line of code.
        start_index: The starting index of the block, used for error messages.

    Returns:
        A list of error messages highlighting issues with the block's formatting
        or content.
    """
    import A_GIS.Code.Unit.to_string
    import A_GIS.Code.Unit._has_imports
    import A_GIS.Code.Unit._wrap_single_block

    # Iterate through each line of the block
    msg = []
    is_body, has_internal_comments = False, False
    for line_number, line_content in enumerate(block):
        # Check for comments at the beginning of the block
        if line_number == 0 and not line_content.lstrip().startswith("#"):
            msg.append(
                "The following block must start with a comment!\n"
                + A_GIS.Code.Unit.to_string(
                    unit=A_GIS.Code.Unit._wrap_single_block(code_body=block),
                    start_index=start_index,
                )
            )

        # Ensure that after code starts, no internal comments appear
        else:
            if not line_content.lstrip().startswith("#"):
                is_body = True
            if is_body and line_content.lstrip().startswith("#"):
                has_internal_comments = True

        # Check for import statements outside the allowed first block
        if A_GIS.Code.Unit._has_imports(block=block):
            msg.append(
                "Imports are only allowed in the first block!\n"
                + A_GIS.Code.Unit.to_string(
                    unit=A_GIS.Code.Unit._wrap_single_block(code_body=block),
                    start_index=start_index,
                )
            )

    # Add a message if internal comments were found after code started
    if has_internal_comments:
        msg.append(
            "The following block should not have internal comments!\n"
            + "All comments should be at the start of the block.\n"
            + A_GIS.Code.Unit.to_string(
                unit=A_GIS.Code.Unit._wrap_single_block(code_body=block),
                start_index=start_index,
            )
        )

    return msg
