import re


def sanitize_model_and_branch_names(model: str, branch: str = "main") -> (str, str):
    """
    Sanitizes and validates the model and branch names for downloading models.

    Args:
        model (str): The model name, potentially including URL and branch information.
        branch (str): The branch name with a default value of 'main'.

    Returns:
        (str, str): A tuple containing the sanitized model and branch names.

    Raises:
        ValueError: If the branch name contains invalid characters.

    Example:
        sanitized_model, sanitized_branch = sanitize_model_and_branch_names(
            model='https://huggingface.co/facebook/opt-1.3b', branch='dev'
        )
    """
    base = "https://huggingface.co"

    # Strip trailing slash from model name
    if model.endswith("/"):
        model = model[:-1]

    # Remove base URL if present
    if model.startswith(base + "/"):
        model = model[len(base) + 1 :]

    # Split model name and branch if included in model
    model_parts = model.split(":")
    model = model_parts[0] if len(model_parts) > 0 else model
    branch = model_parts[1] if len(model_parts) > 1 else branch

    # Validate branch name
    if branch is None:
        branch = "main"
    else:
        pattern = re.compile(r"^[a-zA-Z0-9._-]+$")
        if not pattern.match(branch):
            raise ValueError(
                "Invalid branch name. Only alphanumeric characters, period, underscore, and dash are allowed."
            )

    return model, branch
