def insert_block_placeholders(
    *,
    text: str,
    label: str = "__PLACEHOLDER__",
    block_name: str = r"\S*",
    opening: str = "```",
    closing: str = "```",
):
    """Insert placeholders for blocks"""
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
