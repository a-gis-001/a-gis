def _process_issue(*, issue, store_dir, defect_id_key="sdl"):
    """Preprocess a user-facing gitlab issue with full paths to images.

    issue is the result of a gitlab issue extraction formatted for A_GIS

    store_dir is the root directory for images

    Assumes:
      - product labels are upper case
      - AKA have the form 'Name (from Work)'

    """
    import re
    import pathlib

    def remove_html_comments(text):
        """Removes all HTML comments from the given text."""
        return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    def get_product_labels(labels):
        """Get the product labels as the upper case labels."""
        return [label for label in labels if label.upper() == label]

    def extract_name_and_work(expression):
        """Extract the names and fictional work."""
        match = re.match(r"(.+?)\s*(?:\((.*?)\))?$", expression)
        if match:
            name = match.group(1).strip()
            work = match.group(2).strip() if match.group(2) else None
            return name, work
        return None, None  # In case of unexpected input

    def get_affected_labels(labels):
        """Get the labels that describe affected versions."""
        return [
            label
            for label in labels
            if label.startswith(("awaiting", "will not", "fixed"))
        ]

    d = remove_html_comments(issue["description"])
    i = d.index("## SQA")

    weight = issue["weight"]
    if weight <= 4:
        severity = "MINOR"
    elif weight <= 32:
        severity = "MODERATE"
    elif weight <= 256:
        severity = "SIGNIFICANT"
    else:
        severity = "SAFETY-SIGNIFICANT"

    title = issue[defect_id_key]

    aka = "None"
    if "aka" in issue and issue["aka"] is not None:
        if issue["aka"] != "None":
            aka = issue["aka"]
            name, work = extract_name_and_work(aka)
            title += '    aka "' + name + '"'

    u = f"""
<h2 class="defect-{severity}" id="{issue[defect_id_key]}"> {title} </h2>

**Severity**: <span class="tooltip-{severity}">{severity}</span> (weight=<span class="weight">{weight}</span>)

**Impacted Products**: <span class="products">{', '.join(get_product_labels(issue['labels']))}</span>

**Affected Releases**: {', '.join(get_affected_labels(issue['labels']))}

**External Identifier**: {issue[defect_id_key]}

**AKA**: <span class="aka"> {aka} </span>

**Internal Identifier**: <a href="{issue['url']}">{issue['iid']}</a>

{d[:i]}
"""
    # increase level so top heading is h2
    u = re.sub(r"^#", "##", u, flags=re.MULTILINE)

    for image in issue["images"]:
        # print(image)
        u = u.replace(
            image["link"],
            str((pathlib.Path(store_dir) / image["path"]).resolve()),
        )
    return u
