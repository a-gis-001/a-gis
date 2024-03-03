def apply_patch(*, text: str, patch: str):
    """
    Apply a unified diff to a string.

    Parameters:
    original_text (str): The original text to which the diff will be applied.
    unified_diff (str): The unified diff as a string.

    Returns:
    str: The modified text after applying the diff.
    """
    from diff_match_patch import diff_match_patch

    dmp = diff_match_patch()

    # Convert the unified diff string to a list of Patch objects
    patches = dmp.patch_fromText(patch)

    # Apply the patches to the original text
    patched_text, _ = dmp.patch_apply(patches, text)

    return patched_text
