def get_report_script(
    *,
    products=[],
    severity={
        "SAFETY-SIGNIFICANT": {
            "description": "Undetectable error with magnitude that could invalidate safety analyses",
            "allowed_weights": [512],
            "defaultIdOnly": False,
            "defaultShowDesc": True,
            "defaultHideAll": False,
        },
        "SIGNIFICANT": {
            "description": "Difficult to detect error; results are unreliable for decision-making",
            "allowed_weights": [64, 128, 256],
            "defaultIdOnly": False,
            "defaultShowDesc": True,
            "defaultHideAll": False,
        },
        "MODERATE": {
            "description": "Obvious deviation or performance issue including code crash; low chance of false conclusions",
            "allowed_weights": [8, 16, 32],
            "defaultIdOnly": False,
            "defaultShowDesc": False,
            "defaultHideAll": False,
        },
        "MINOR": {
            "description": "Cosmetic or negligible; does not alter conclusions of analysis",
            "allowed_weights": [1, 2, 4],
            "defaultIdOnly": True,
            "defaultShowDesc": False,
            "defaultHideAll": True,
        },
    },
):
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
    js_output = template.render(severity=severity)
    return js_output
