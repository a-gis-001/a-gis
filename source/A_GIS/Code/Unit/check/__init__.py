def check(*, unit: type["A_GIS.Code.Unit._Unit"]) -> list[str]:
    """
    Checks a list of code unit to ensure they meet specific requirements regarding import statements and comment usage.

    The function validates that:
    - The first code block may optionally contain absolute imports.
    - All subsequent code unit must start with one or more comment lines, followed by code, and optionally end with a blank line.

    Args:
        unit: A list of code unit, where each block is a list of strings, with each string representing a line of code.

    Returns:
        A list of strings, where each string is a message detailing any violations found within the code unit.
    """
    import A_GIS.Code.Unit._has_imports
    import A_GIS.Code.Unit._check_imports
    import A_GIS.Code.Unit._check_body_block

    # Initialize a list to accumulate messages
    msg = []
    for i, block in enumerate(unit.code_body):

        # Special checks for the first block, which could contain imports
        is_import_block = False
        if i == 0:
            msg.extend(
                A_GIS.Code.Unit._check_imports(block=block, start_index=i)
            )
            is_import_block = A_GIS.Code.Unit._has_imports(block=block)

        # For non-import unit, perform body block checks
        if not is_import_block:
            msg.extend(
                A_GIS.Code.Unit._check_body_block(block=block, start_index=i)
            )

    # Return list of messages.
    return msg
