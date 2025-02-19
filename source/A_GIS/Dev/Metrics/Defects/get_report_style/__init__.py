def get_report_style(*, severity_definitions):
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
    css_output = template.render(SEVERITY_DEFINITIONS=severity_definitions)
    return css_output
