def get_patch(*, initial: str, final: str):
    """
    Generates the unified diff from the initial to final string.

    Parameters:
    initial: A string representing the initial state.
    final: A string representing the final state.

    Returns:
    A string representing the unified diff between the initial and final states.
    """
    from diff_match_patch import diff_match_patch

    dmp = diff_match_patch()
    patches = dmp.patch_make(initial, final)
    return dmp.patch_toText(patches)
