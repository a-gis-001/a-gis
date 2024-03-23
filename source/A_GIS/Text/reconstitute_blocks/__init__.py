def reconstitute_blocks(*, text: str, subs: dict):
    """Reconstitute the blocks of text that were placeholders

    The function takes a larger block of text and replaces each
    placeholder with its corresponding block from a given dictionary.
    It uses the `A_GIS.Text.replace_block` function to perform
    this operation.

    Args:
        text (str): The main block of text where placeholders are
                    replaced by blocks.
        subs (dict): A dictionary where keys represent placeholders
                     in the text and values are the corresponding blocks
                     that will replace them.

    Raises:
        None

    Returns:
        str: The original text with all placeholders replaced by their
             respective blocks.
    """

    import A_GIS.Text.replace_block

    for placeholder, block in subs.items():
        text = A_GIS.Text.replace_block(
            text=text, find_block=placeholder, replace_with=block
        )
    return text
