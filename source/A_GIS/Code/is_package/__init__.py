def is_package(*, code: str, file_name: str = ""):
    # True if file is named __init__.py and primarily contains imports
    import A_GIS.Code.distill

    if file_name == "__init__.py":
        return True

    code0 = A_GIS.Code.distill(code=code)
    for line in code0.split("\n"):
        if not line.startswith("from"):
            return False

    return True
