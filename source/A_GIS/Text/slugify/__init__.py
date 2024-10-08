def slugify(*, name: str):
    """Create a slug from some name."""
    import re

    value = name.lower()
    value = re.sub(r"[\s]+", "-", value)
    value = re.sub(r"[^\w\-]", "", value)
    return value
