def get(*, label: str, prefix: str = "", postfix: str = ""):
    """Load a prompt from locally stored ones"""

    system = """
    You are a helpful assistant.
    """

    user = f"""
    Answer the question in one sentence maximum. If you do not know, guess.
    """

    return system, user
