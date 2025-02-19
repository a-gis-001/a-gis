def get_report_script(*, products, severity_definitions):
    """Get the defect report scripts you need.

    The severity definitions are passed in a dictionary with the top-level keys
    for the names of the severity levels. The value is a dictionary with the description,
    allowed weights, and default values for filter boxes.
    """
    import jinja2
    import os

    # Load the Jinja template
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    )
    template = template_env.get_template("report.js")

    # Render the template with the provided levels
    js_output = template.render(
        PRODUCTS=products, SEVERITY_DEFINITIONS=severity_definitions
    )
    return js_output
