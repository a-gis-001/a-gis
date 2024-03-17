def Code__distill(*, code: str) -> str:
    import ast
    import re
    import A_GIS.Code._distill_imports
    parsed = ast.parse(code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            node.value = ast.Constant(value='')
    distilled_code = A_GIS.Code._distill_imports(code=code)
    distilled_code = re.sub('^\\s*""""""\\s*$\\n', '', ast.unparse(parsed), flags=re.MULTILINE)
    distilled_code = re.sub('\\n\\s*\\n', '\n', distilled_code)
    return distilled_code