def format_issue(*, issue, severity_definitions, base_path="."):
    """Do a full formatting of an issue to html."""
    import markdown
    import A_GIS.Dev.Metrics.Defects._process_issue
    import A_GIS.Dev.Metrics.Defects._convert_math_blocks
    import A_GIS.Dev.Metrics.Defects._convert_inline_math

    # Get base markdown that has a bunch of junk removed.
    md_content = A_GIS.Dev.Metrics.Defects._process_issue(
        issue=issue, store_dir=base_path, severity_definitions=severity_definitions
    )

    # Convert to HTML.
    html_content = markdown.markdown(
        md_content, extensions=["extra", "fenced_code"]
    )

    # Fix math blocks and inline math.
    html_content = A_GIS.Dev.Metrics.Defects._convert_math_blocks(html_content)
    html_content = A_GIS.Dev.Metrics.Defects._convert_inline_math(html_content)

    # Embed images.
    html_with_images = A_GIS.Text.Html.embed_images(
        html=html_content, base_path=base_path
    )

    return html_with_images
