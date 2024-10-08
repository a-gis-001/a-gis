def get_links(*, markdown: str):
    """Extract hyperlinks from Markdown text as a structured object.

    This function processes a string of Markdown content to identify and
    extract all links in the format `[display text](URL)`. It uses a
    regular expression to find these links and then organizes them into
    a list of tuples, each containing the display text and the URL. This
    list is then encapsulated into a structured object using
    `A_GIS.Code.make_struct`.

    Args:
        markdown (str):
            A string containing Markdown-formatted text from which to
            extract links.

    Returns:
        dataclass:
            With the following attributes

            - links (list of tuples): Each tuple contains two
              elements, the first is a string representing the link's
              display text, and the second is a string representing
              the link's URL.
            - _markdown (str): The original Markdown content processed
              for extracting links.
    """
    import A_GIS.Code.make_struct
    import re

    # Regular expression to find all Markdown links in the form [text](url)
    pattern = r"\[([^\]]+)\]\((http[s]?://[^\)]+)\)"

    # Find all matches in the Markdown content
    matches = re.findall(pattern, markdown)

    # Print each link's text and URL
    links = []
    for text, url in matches:
        links.append((text, url))

    return A_GIS.Code.make_struct(links=links, _markdown=markdown)
