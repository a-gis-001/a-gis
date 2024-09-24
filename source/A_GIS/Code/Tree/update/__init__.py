def update(*, tree: dict):
    """Update a tree structure, optionally generating package imports.

    This function recursively processes a dictionary representing a tree
    structure that defines Python package contents. It updates the tree
    by calling itself on each nested item within the tree. If the top-
    level tree contains a `_type` key with the value `"package"`, the
    function will collect import statements for all functions, classes,
    and sub-packages within the package. These import statements are
    then written to a file specified by the `_file` key in the tree
    dictionary. If no `_type` or `_file` is present, or if the `_type`
    is not `"package"`, the function simply recurses through the tree
    without generating any import statements.

    After processing all nested items, if import statements were
    collected, they are written to the specified file, optionally re-
    formatting the code using `A_GIS.Code.reformat`. If no imports are
    found, the function will write the original content of the file back
    to the file after re-formatting.

    Args:
        tree (dict):
            A dictionary representing the tree structure to be updated.
            This should contain keys for `"_type"` and `"_file"` when
            updating a package. The nested dictionaries represent
            functions, classes, or sub-packages, each potentially
            containing their own `_type` and `_file`.

    Returns:
        None:
            The function updates the tree in place and writes to the
            file system as needed.
    """
    import A_GIS.File.write
    import A_GIS.File.read
    import A_GIS.Code.reformat

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
