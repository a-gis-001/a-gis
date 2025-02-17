def _convert_math_blocks(html_content):
    """Convert <pre><code class="language-math">...</code></pre> to KaTeX-compatible $$ ... $$."""
    import bs4

    soup = bs4.BeautifulSoup(html_content, "html.parser")

    for code_block in soup.find_all("code", class_="language-math"):
        # Ensure it is inside <pre>
        if code_block.parent.name == "pre":
            math_content = code_block.get_text(
                strip=True
            )  # Extract math content

            # Create a new KaTeX-compatible block
            new_math_block = soup.new_tag("p")
            new_math_block.string = f"$$\n{math_content}\n$$"

            # Replace <pre><code> with the new math block
            code_block.parent.replace_with(new_math_block)

    return str(soup)
