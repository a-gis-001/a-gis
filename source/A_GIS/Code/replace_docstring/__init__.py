def replace_docstring(*, code: str, docstring) -> str:
    """Add or replaces the docstring of the first class or function in provided code, appending if no existing docstring is found.

    This function searches for the first class or function definition in the provided code and replaces its existing docstring with the new one provided. If no docstring is found, it adds a new docstring at the end of the class or function definition.

    Args:
        code (str):
            The original Python code containing the definitions to be modified.
        docstring (str):
            The new docstring to be added or replaced, including its triple-quoted
            string format.

    Returns:
        str:
            A string containing the modified code with the updated docstring for the first class or function definition found.

    Raises:
        ValueError:
            If no class or function definitions are found in the code, indicating that there is nothing to replace or add.
    """

    import re

    if not isinstance(docstring, str):
        docstring = str(docstring)

    # Pattern to match class or function definitions (including multiline
    # signatures and return types)
    pattern = re.compile(
        r'^(class\s+\w+|def\s+\w+)\s*\(.*?\)(?:\s*->\s*.*?)?\s*:\s*(""".*?""")?',
        re.DOTALL | re.MULTILINE,
    )

    # Format the new docstring
    if docstring is None:
        formatted_docstring = ""
    else:
        docstring = docstring.strip()
        formatted_docstring = f'"""{docstring}\n"""\n'

    # Function to replace or add the docstring
    def _replace_match(match):
        existing_docstring = match.group(2)
        if existing_docstring:
            # Replace existing docstring
            return match.group(0).replace(
                existing_docstring, formatted_docstring
            )
        else:
            # Add new docstring after the function or class signature
            return f"{match.group(0)}\n    {formatted_docstring}"

    # Replace or add the docstring in the first class or function definition
    new_code, num_replacements = pattern.subn(_replace_match, code, count=1)

    return new_code
