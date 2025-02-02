def _extract_sdl(issue_text):
    """Extract the SDL number from issue description.

    Args:
        issue_text (str): Issue description text.

    Returns:
        str: SDL number if found, None otherwise.
    """
    import re

    # Match the ## SQA section and look for the Change log number within it
    sqa_section = re.search(r"## SQA(.*?)(##|$)", issue_text, re.DOTALL)
    if sqa_section:
        # Extract the content of the ## SQA section
        sqa_content = sqa_section.group(1)
        # Look for the Change log number within the ## SQA section
        defect_log_match = re.search(
            r"Defect log number:\s*(SDL-\d{4}-\d{3})", sqa_content
        )
        if defect_log_match:
            return defect_log_match.group(1)
    return None
