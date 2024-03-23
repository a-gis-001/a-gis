def reconstitute_blocks(*, text: str, subs: dict):
    """Reconstitute the blocks that you inserted placeholders for"""
    import A_GIS.Text.replace_block

    for placeholder, block in subs.items():
        text = A_GIS.Text.replace_block(
            text=text, find_block=placeholder, replace_with=block
        )
    return text
