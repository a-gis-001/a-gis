def insert_block_placeholders(
    *,
    text: str,
    label: str = "__PLACEHOLDER__",
    block_name: str = "",
    opening: str = "```",
    closing: str = "```",
):
    """Inserts placeholders for blocks of specified type in a given text.

    This function scans the input `text` for all blocks of specified type (default is 'python')
    and replaces each block with a unique placeholder string (default is '__PLACEHOLDER__'). The
    original blocks are stored in a dictionary, where keys are placeholders and values are the
    corresponding original blocks.

    Args:
        text (str): Input text to process.
        label (str, optional): Label for placeholder strings. Defaults to '__PLACEHOLDER__'.
        block_name (str, optional): Type of block to replace. Defaults to 'python'.
        opening (str, optional): Opening string denoting the start of a block.
                                 Defaults to '```'.
        closing (str, optional): Closing string denoting the end of a block.
                                Defaults to '```'.

    Raises:
        None

    Returns:
        tuple: A tuple containing two elements:
            - subs (dict): Dictionary where keys are placeholders and values are original blocks.
            - text (str): Modified input `text` with placeholders in place of the original blocks.
    """

    import A_GIS.Text.extract_markdown
    import A_GIS.Text.replace_block

    block = " "
    subs = {}
    i = 0
    while block != "" and i < 10000:
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
