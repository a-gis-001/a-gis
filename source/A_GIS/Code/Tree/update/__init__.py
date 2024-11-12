def update(*, tree: dict):
    """Update the code structure represented by a dictionary.

    This function recursively updates the code structure provided in
    `tree`. If the tree represents a package, it generates import
    statements for its functions, classes, and sub-packages. It then
    writes these imports back to the package's file along with any
    existing docstring. For individual files (non-package), it reformats
    the code and writes it back to the file.

    Args:
        tree (dict):
            A dictionary representing a code structure. If it contains
            `_type` key with value "package", it is treated as a package
            containing sub-packages, functions, and classes. Each item
            in the tree can be recursively another tree or a file path.
    """
    import A_GIS.File.write
    import A_GIS.File.read
    import A_GIS.Code.reformat

    imports = None
    is_package = False
    if "_type" in tree:
        if tree["_type"] == "package":
            is_package=True
            imports = {"Functions": [], "Classes": [], "Packages": []}
    for name in tree:
        if name.startswith('_'):
            continue
        if is_package:
            if tree[name]["_type"] == "package":
                imports["Packages"].append(f"from . import {name}")
            elif tree[name]["_type"] == "function":
                imports["Functions"].append(f"from .{name} import {name}")
            elif tree[name]["_type"] == "class":
                imports["Classes"].append(f"from .{name} import {name}")

        update(tree=tree[name])

    if is_package:
        existing = A_GIS.File.read(file=tree["_file"])
        docstring = (
            A_GIS.Code.parse_docstring(code=existing, clean=False) or ""
        )
        code = f'"""{docstring}\n"""\n'
        first = True
        for k, v in imports.items():
            if len(v) > 0:
                if not first:
                    code += "\n"
                first = False
                code += "# {}\n{}\n".format(k, "\n".join(sorted(v)))
        A_GIS.File.write(content=code, file=tree["_file"])
    elif "_file" in tree:
        code = A_GIS.File.read(file=tree["_file"])
        A_GIS.File.write(
            content=A_GIS.Code.reformat(code=code), file=tree["_file"]
        )
