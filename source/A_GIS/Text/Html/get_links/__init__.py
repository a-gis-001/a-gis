def get_links(*, html: str):
    """Extract hyperlinks from an HTML document.

    This function takes a string `html` containing HTML content and
    extracts all the links (`<a>` tags) from it using BeautifulSoup. It
    then organizes these links into a list of tuples, each containing
    the text displayed for the link and its corresponding URL (`href`
    attribute). The function returns an object created by
    `A_GIS.Code.make_struct` with two attributes: `links`, which is a
    list of tuples as described above, and `_html`, which contains the
    original HTML string.

    Args:
        html (str):
            A string containing well-formed HTML that you want to parse
            for links.

    Returns:
        dataclass:
            With the following attributes

            - links (list of tuple): Each tuple contains the text and
              href of a link found in the HTML.
            - _html (str): The original HTML content from which the
              links were extracted.
    """
    import bs4
    import A_GIS.Code.make_struct

    # Parse the HTML content with BeautifulSoup
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Print each link's href and text
    links = []
    for a in soup.find_all("a"):
        links.append((a.get_text(), a.get("href")))

    return A_GIS.Code.make_struct(links=links, _html=html)
