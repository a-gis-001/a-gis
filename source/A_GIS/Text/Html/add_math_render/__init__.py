def add_math_render() -> str:
    """Generate HTML code to enable KaTeX math rendering in a webpage.
    
    This function returns the necessary HTML code to enable KaTeX math rendering
    in a webpage. It includes:
    1. KaTeX CSS for styling
    2. KaTeX JS for math rendering
    3. Auto-render extension for automatic math detection
    4. Initialization script with configuration
    
    The math delimiters are configured as:
    - Inline math: Single dollar signs ($...$)
    - Display math: Double dollar signs ($$...$$)
    
    Math rendering is ignored in the following HTML tags:
    - script
    - noscript
    - style
    - textarea
    - pre
    - code
    
    Example:
        >>> html_content = "<html><head>{}</head><body>$x^2$</body></html>"
        >>> print(html_content.format(A_GIS.Text.Html.add_math_render()))
    
    Returns:
        str: HTML code block containing KaTeX setup (CSS, JS, and initialization)
    """
    return """
<!-- KaTeX CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css" data-katex>
<!-- KaTeX JS -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js" data-katex></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/contrib/auto-render.min.js" data-katex></script>
<script id="katex-init" data-katex>
    document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$", display: false }
            ],
            ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
        });
    });
</script>
    """
