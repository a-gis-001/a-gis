def add_math_render():
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
