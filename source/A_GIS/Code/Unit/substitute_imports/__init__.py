def substitute_imports(*, code: str):
    """Substitute the A_GIS import statements with actual code.

    Currently only supports one level of recursion.

    """
    import A_GIS.Code.Unit.read
    import A_GIS.Code.make_struct
    import A_GIS.Text.replace_block
    import re

    expanded_code = code
    subs = []
    for found in re.finditer(r"^(\s*)import (A_GIS\..*)", code, re.MULTILINE):
        indent = found.group(1)
        name = found.group(2)
        subs.append(name)
        replace_with = A_GIS.Code.Unit.read(name=name).code
        replace_with = "\n".join(
            [indent + x for x in replace_with.splitlines()]
        )
        expanded_code = expanded_code.replace(found.group(0), replace_with)

    return A_GIS.Code.make_struct(
        initial_code=code, subs=subs, code=expanded_code
    )
