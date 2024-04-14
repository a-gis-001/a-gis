def check(*, unit: type["A_GIS.Code.Unit._Unit"]) -> list[str]:
    """
    Checks a "unit" to ensure they meet specific
    requirements regarding import statements and comment usage.

    The function validates that:

    - The first code block may optionally contain absolute imports.
    - All subsequent code unit must start with one or more comment
      lines, followed by code, and optionally end with a blank line.

    Args:
        unit: a special function designed to be small and independent.

    Returns:
        A list of strings, where each string is a message detailing
        any violations found within the code unit.
    """
    import A_GIS.Code.Unit._has_imports
    import A_GIS.Code.Unit._check_imports
    import A_GIS.Code.Unit._check_body_block

    # Iterate through code body and accumulate error messages.
    errors = []
    for i, block in enumerate(unit.code_body):
        # Determine if first block is an import block.
        is_import_block = i == 0 and A_GIS.Code.Unit._has_imports(block=block)

        # Perform checks based on import block or not.
        if is_import_block:
            errors.extend(
                A_GIS.Code.Unit._check_imports(block=block, start_index=i)
            )
        else:
            errors.extend(
                A_GIS.Code.Unit._check_body_block(block=block, start_index=i)
            )

    # Return list of messages.
    return errors
