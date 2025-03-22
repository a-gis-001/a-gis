def insert_block_placeholders(
    *,
    text: str,
    label: str = "__PLACEHOLDER__",
    block_name: str = "",
    opening: str = "```",
    closing: str = "```",
    max_blocks: int = 10000,
):
    """Inserts placeholders for blocks of specified type in a given text.

    This function scans the input text for all blocks of specified
    type (default is 'python') and replaces each block with a unique
    placeholder string (default is '__PLACEHOLDER__'). The original
    blocks are stored in a dictionary, where keys are placeholders and
    values are the corresponding original blocks.

    Args:
        text: Input text to process
        label: Label to use for placeholders
        block_name: Name of the block type to process
        opening: Opening delimiter for blocks
        closing: Closing delimiter for blocks
        max_blocks: Maximum number of blocks to process

    Returns:
        Dictionary mapping placeholders to original blocks
    """

    import A_GIS.Text.extract_markdown
    import A_GIS.Text.replace_block

    block = " "
    subs = {}
    i = 0
    while block != "" and i < max_blocks:
        block = A_GIS.Text.extract_markdown(
            text=text,
            content_only=False,
            block_name=block_name,
            opening=opening,
            closing=closing,
            dedent_result=True,
        )
        if block != "":
            i += 1
            placeholder = label + str(i)
            subs[placeholder] = block
            text = A_GIS.Text.replace_block(
                text=text, find_block=block, replace_with=placeholder
            )
    return subs, text
