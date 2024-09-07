def extract_python(*, text: str):
    """Extract python code from an AI-generated response"""
    import A_GIS.Text.extract_markdown
    import A_GIS.Code.distill
    import A_GIS.Code.replace_from_imports
    import A_GIS.Code.canonicalize_imports
    import A_GIS.Code.reformat

    code = A_GIS.Text.extract_markdown(text=text, block_name="python")

    try:
        code = A_GIS.Code.distill(code=code)
        code = A_GIS.Code.reformat(code=code)
    except BaseException:
        pass

    return code
