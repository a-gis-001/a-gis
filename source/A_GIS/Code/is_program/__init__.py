def is_program(*, code: str, file_name: str = ""):
    # Checks if file is named __main__.py or contains sys.argv
    if file_name == "__main__.py":
        return True

    if "sys.argv" in code:
        return True

    return False
