def fix_links(*, markdown: str, links):
    """Replace URLs in markdown with their corresponding embeddings.

    This function processes a given markdown string to replace each URL
    found within it with its associated embedding vector. It first
    retrieves all the links present in the markdown and then calculates
    the embedding for each URL using the
    `A_GIS.Text.calculate_embedding` function. After obtaining the
    embeddings, it compares each markdown link's embedding with those of
    the provided URLs to find the most similar match. If a matching URL
    is found, the original URL in the markdown is replaced with the
    matched URL.

    The function returns a structured object containing:

    - The modified markdown string with URLs replaced by their
      corresponding embeddings.
    - A list of embedding vectors for all the URLs present in the
      markdown.
    - The original list of links from the markdown.
    - The original list of URLs provided to the function.
    - The original markdown string.

    Args:
        markdown (str):
            The markdown content to be processed.
        links (list of tuple):
            A list where each element is a tuple containing the name and
            URL of a link.

    Returns:
        dataclass:
            With the following attributes

            - markdown (str): The modified markdown string with URLs
              replaced by their corresponding embeddings.
            - embeddings (list of numpy.ndarray): A list of embedding
              vectors for all the URLs present in the markdown.
            - markdown_embeddings (list of numpy.ndarray): The same
              list of embedding vectors as above, duplicated for
              consistency with the return type specified.
            - markdown_links (list of tuple): The original list of
              links from the markdown.
            - _links (list of tuple): The provided list of URLs and
              names, unchanged.
            - _markdown (str): The original markdown string provided
              as input to the function.
    """
    import A_GIS.Text.calculate_embedding
    import A_GIS.Text.Markdown.get_links
    import sklearn.metrics.pairwise
    import numpy
    import A_GIS.Code.make_struct

    embeddings = []
    for link in links:
        _, e, _ = A_GIS.Text.calculate_embedding(
            lines=[f"Name: {link[0]}", "URL: {link[1]}"], nchunks=1
        )
        embeddings.append(numpy.array(e[0]))

    md_links = A_GIS.Text.Markdown.get_links(markdown=markdown).links
    md_embeddings = []
    new_markdown = markdown
    for md_link in md_links:
        _, e, _ = A_GIS.Text.calculate_embedding(
            lines=[f"Name: {md_link[0]}", f"URL: {md_link[1]}"], nchunks=1
        )
        query = numpy.array(e[0]).reshape(1, -1)
        similarities = sklearn.metrics.pairwise.cosine_similarity(
            query, embeddings
        )
        best_index = numpy.argmax(similarities)
        new_markdown = new_markdown.replace(md_link[1], links[best_index][1])

    return A_GIS.Code.make_struct(
        markdown=new_markdown,
        embeddings=embeddings,
        markdown_embeddings=md_embeddings,
        markdown_links=md_links,
        _links=links,
        _markdown=markdown,
    )
