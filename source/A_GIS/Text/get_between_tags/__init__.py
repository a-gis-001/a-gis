def get_between_tags(
    *, text: str, begin_tag: str = "<tag>", end_tag: str = "</tag>"
):
    """Extract and returns the string content sandwiched between text.

    This function utilizes `A_GIS.Text.get_before_tag` and
    `A_GIS.Text.get_after_tag` to first find the content after the beginning tag,
    then finds the content before the ending tag, and finally concatenates these
    two substrings to return the content between the specified tags. If the beginning
    or ending tags are not found within the text, an empty string is returned.

    Args:
        text (str): The input text from which to extract content.
        begin_tag (str, optional): The opening tag used to identify the start of the
            content to be extracted. Defaults to `"<tag>"`.
        end_tag (str, optional): The closing tag used to identify the end of the
            content to be extracted. Defaults to `"</tag>"`.

    Returns:
        str: A string containing the text that is situated between the specified
        begin and end tags if they are found within the input text; otherwise, an
        empty string.

    Raises:
        None
    """

    import A_GIS.Text.get_before_tag
    import A_GIS.Text.get_after_tag

    return A_GIS.Text.get_before_tag(
        text=A_GIS.Text.get_after_tag(text=text, tag=begin_tag), tag=end_tag
    )
