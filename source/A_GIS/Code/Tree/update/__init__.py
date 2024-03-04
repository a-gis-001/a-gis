def update(*, tree: dict):
    """Update the package files throughout the files listed in the tree to have
    the correct format and content."""
    import A_GIS.File.write
    import A_GIS.File.read
    import A_GIS.Code.format

    imports = None
    if "_type" in tree:
        if tree["_type"] == "package":
            imports = {"Functions": [], "Classes": [], "Packages": []}
    for name in tree:
        if name in set(["_type", "_file"]):
            continue
        if imports:
            if tree[name]["_type"] == "package":
                imports["Packages"].append(f"from . import {name}")
            elif tree[name]["_type"] == "function":
                imports["Functions"].append(f"from .{name} import {name}")
            elif tree[name]["_type"] == "class":
                imports["Classes"].append(f"from .{name} import {name}")

        update(tree=tree[name])

    if imports:
        code = ""
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
            content=A_GIS.Code.format(code=code), file=tree["_file"]
        )
