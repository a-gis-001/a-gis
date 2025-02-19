def get_report(
    *,
    issues,
    title=None,
    date=None,
    store_dir=None,
    toc=True,
    products=["All"],
    severity_definitions={
        "SAFETY-SIGNIFICANT": {
            "description": "Undetectable error with magnitude that could invalidate safety analyses",
            "allowed_weights": [512],
            "default_id_only": False,
            "default_show_desc": True,
            "default_hide_all": False,
            "border_color": "hsla(0, 95%, 75%, 0.5)",
            "bg_color": "hsla(0, 95%, 90%, 0.9)",
        },
        "SIGNIFICANT": {
            "description": "Difficult to detect error; results are unreliable for decision-making",
            "allowed_weights": [64, 128, 256],
            "default_id_only": False,
            "default_show_desc": True,
            "default_hide_all": False,
            "border_color": "hsla(30, 95%, 75%, 0.5)",
            "bg_color": "hsla(30, 95%, 90%, 0.9)",
        },
        "MODERATE": {
            "description": "Obvious deviation or performance issue including code crash; low chance of false conclusions",
            "allowed_weights": [8, 16, 32],
            "default_id_only": False,
            "default_show_desc": False,
            "default_hide_all": False,
            "border_color": "hsla(50, 95%, 75%, 0.5)",
            "bg_color": "hsla(50, 95%, 90%, 0.9)",
        },
        "MINOR": {
            "description": "Cosmetic or negligible; does not alter conclusions of analysis",
            "allowed_weights": [1, 2, 4],
            "default_id_only": True,
            "default_show_desc": False,
            "default_hide_all": True,
            "border_color": "hsla(0, 0%, 75%, 0.4)",
            "bg_color": "hsla(0, 0%, 90%, 0.9)",
        },
    },
):
    """Get an HTML defects report."""
    import A_GIS.Dev.Metrics.Defects.get_report_style
    import A_GIS.Dev.Metrics.Defects.get_report_script
    import A_GIS.Text.Html.add_math_render

    body = ""
    for v in issues:
        body += (
            "\n<section>\n"
            + A_GIS.Dev.Metrics.Defects.format_issue(
                issue=v, base_path=store_dir, severity_definitions=severity_definitions
            )
            + "\n</section>\n"
        )

    if title:
        title = f"<h1>{title}</h1>"
    else:
        title = ""
    if date:
        date = f"<p><strong>Last Updated: </strong> {date}</p>"
    else:
        date = ""
    if toc:
        toc_html = '<div id="inline-toc"></div>'
    else:
        toc_html = ""

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>

{A_GIS.Text.Html.add_math_render()}

<style>
{A_GIS.Dev.Metrics.Defects.get_report_style(severity_definitions=severity_definitions)}
</style>
</head>
<body>

<div id="content">

<div id="info-container">
{title}
{date}
<p><strong>Product Filter: </strong><span id="dropdown-container"></span></p>
{toc_html}
</div>

<div class="thick-divider"></div>

{body}

</div>

<script>
{A_GIS.Dev.Metrics.Defects.get_report_script(products=products,severity_definitions=severity_definitions)}
</script>

</body>
</html>
"""
