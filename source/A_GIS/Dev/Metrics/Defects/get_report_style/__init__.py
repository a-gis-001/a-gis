def get_report_style(
    *,
    levels={
        "MINOR": {
            "border_color": "hsla(0, 0%, 75%, 0.4)",
            "bg_color": "hsla(0, 0%, 90%, 0.9)",
        },
        "MODERATE": {
            "border_color": "hsla(50, 95%, 75%, 0.5)",
            "bg_color": "hsla(50, 95%, 90%, 0.9)",
        },
        "SIGNIFICANT": {
            "border_color": "hsla(30, 95%, 75%, 0.5)",
            "bg_color": "hsla(30, 95%, 90%, 0.9)",
        },
        "SAFETY-SIGNIFICANT": {
            "border_color": "hsla(0, 95%, 75%, 0.5)",
            "bg_color": "hsla(0, 95%, 90%, 0.9)",
        },
    },
):
    """Generates CSS for defects reporting.

    Args:
        levels (list): A list of dictionaries containing level names and colors.

    Returns:
        str: The generated CSS as a string.
    """
    import jinja2
    import os

    # Load the Jinja template
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    )
    template = template_env.get_template("report.css.jt")

    # Render the template with the provided levels
    css_output = template.render(levels=levels)
    return css_output
