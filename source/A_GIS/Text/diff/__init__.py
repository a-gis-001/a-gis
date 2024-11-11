def diff(*, initial: str, final: str):
    """Compute the difference between two strings.

    This function performs a diff operation using the `diff_match_patch`
    library to find the differences between two input strings, `initial`
    and `final`. It then returns these differences in two formats: as a
    textual representation (a list of diffs) and as an HTML-formatted
    string that can be rendered in a web browser. The results are
    encapsulated within an instance of a struct created by
    `A_GIS.Code.make_struct`.

    Args:
        initial (str):
            The original text or content to compare against.
        final (str):
            The modified text or content that was changed relative to
            `initial`.

    Returns:
        dataclass:
            With the following attributes

            - html (str): An HTML string representing the visual diff
              between `initial` and `final`.
            - diffs (list of str): A list of differences between
              `initial` and `final`, in a format that can be processed
              by `diff_match_patch`.
    """
    import A_GIS.Code.make_struct
    import diff_match_patch.diff_match_patch

    # Create differ object.
    dmp = diff_match_patch.diff_match_patch()
    # Note, could access more diff options here.

    # Do the diff.
    diffs = dmp.diff_main(text1=initial, text2=final)

    # Get an html version of the diff.
    html = dmp.diff_prettyHtml(diffs)

    return A_GIS.Code.make_struct(html=html, diffs=diffs)
