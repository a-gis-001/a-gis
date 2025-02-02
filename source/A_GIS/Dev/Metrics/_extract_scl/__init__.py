def _extract_scl(issue_text):
    """Extract the SCL number from issue description.

    Args:
        issue_text (str): Issue description text.

    Returns:
        str: SCL number if found, None otherwise.
    """
    import re

    # Match the ## SQA section and look for the Change log number within it
    sqa_section = re.search(r"## SQA(.*?)(##|$)", issue_text, re.DOTALL)
    if sqa_section:
        # Extract the content of the ## SQA section
        sqa_content = sqa_section.group(1)
        # Look for the Change log number within the ## SQA section
        change_log_match = re.search(
            r"Change log number:\s*(SCL-\d{4}-\d{3})", sqa_content
        )
        if change_log_match:
            return change_log_match.group(1)
    return None
