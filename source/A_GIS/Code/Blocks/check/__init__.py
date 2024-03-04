def check(*, blocks):
    """Do checks"""
    import A_GIS.Code.Blocks.to_string

    i = 0
    msg = []
    for block in blocks:
        is_body = False
        has_internal_comments = False
        for line in range(len(block)):
            if line == 0:
                if not block[line].lstrip().startswith("#"):
                    msg.append(
                        "The following block must start with a comment!\n"
                        + A_GIS.Code.Blocks.to_string(blocks=[block], start_index=i)
                    )
            else:
                if not block[line].lstrip().startswith("#"):
                    is_body = True
                if is_body and block[line].lstrip().startswith("#"):
                    has_internal_comments = True
        if has_internal_comments:
            msg.append(
                "The following block should not have internal comments! All comments should be a the start of the block.\n"
                + A_GIS.Code.Blocks.to_string(blocks=[block], start_index=i)
            )

        i += 1
    return msg
