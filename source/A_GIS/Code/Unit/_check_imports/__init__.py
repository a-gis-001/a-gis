def _check_imports(*, block: list[str], start_index: int = 0) -> list[str]:
    """Check for correct use of imports within a code block, enforcing absolute
    imports and no comments within import unit.

    This function iterates through each line of the provided code block. It
    checks if the block contains any import statements and validates that all
    import statements are absolute (do not use 'from') and that no comments are
    present within the import block. If any violations are found, appropriate
    error messages are generated, including the context of the block with its
    starting index for easier identification.

    Args:
        block: A list of strings, each representing a line of code in the block.
        start_index: The index of the block within a larger collection, used for
            referencing in error messages.

    Returns:
        A list of strings, with each string being an error message related to
        import statement violations.
    """
    import A_GIS.Code.Unit._has_imports
    import A_GIS.Code.Unit._wrap_single_block
    import A_GIS.Code.Unit.to_string

    # Accumulate into messages if the block contains any import statements.
    msg = []
    if A_GIS.Code.Unit._has_imports(block=block):
        for line in block:

            # Check for non-absolute imports.
            if line.lstrip().startswith("from "):
                msg.append(
                    "Imports must be absolute (no from)!\n"
                    + A_GIS.Code.Unit.to_string(
                        unit=A_GIS.Code.Unit._wrap_single_block(
                            code_body=block
                        ),
                        start_index=start_index,
                    )
                )

            # Check for comments within import unit.
            if line.lstrip().startswith("#"):
                msg.append(
                    "Import unit cannot have comments!\n"
                    + A_GIS.Code.Unit.to_string(
                        unit=A_GIS.Code.Unit._wrap_single_block(
                            code_body=block
                        ),
                        start_index=start_index,
                    )
                )

    # Return final list of messages.
    return msg
