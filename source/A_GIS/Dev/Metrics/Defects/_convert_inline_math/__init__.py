def _convert_inline_math(html_content):
    """Fix inline math expressions by removing <code> tags inside $...$."""
    import bs4
    import re

    soup = bs4.BeautifulSoup(html_content, "html.parser")

    # Convert the soup object to a string and find all inline math blocks
    # ($...$)
    modified_html = str(soup)

    # Regex pattern to match $...$ (excluding newlines)
    inline_math_pattern = re.compile(r"\$(.*?)\$")

    def replace_code_tags(match):
        """Remove <code> tags inside math expressions."""
        math_expr = match.group(1)  # Extract content inside $...$
        math_soup = bs4.BeautifulSoup(math_expr, "html.parser")

        # Replace <code>...</code> with just its content
        for code_tag in math_soup.find_all("code"):
            code_tag.replace_with(code_tag.text)

        return f"${math_soup.text}$"  # Return cleaned-up inline math

    # Apply regex-based replacement
    modified_html = inline_math_pattern.sub(replace_code_tags, modified_html)

    return modified_html
