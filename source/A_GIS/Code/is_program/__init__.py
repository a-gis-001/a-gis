def is_program(*, code: str, filename: str = ""):
    # Checks if file is named __main__.py or contains sys.argv
    if filename == "__main__.py":
        return True

    if "sys.argv" in code:
        return True

    return False
