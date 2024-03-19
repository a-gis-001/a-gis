def find_and_replace(
    *,
    file: type["pathlib.Path"],
    files: list["pathlib.Path"] = None,
    old: str,
    new: str,
    is_regex: bool = False,
):
    """Find and replace in file"""
    import A_GIS.File.read
    import A_GIS.File.write
    import A_GIS.Text.find_and_replace

    if files is None:
        files = [file]
    else:
        files += file

    total_replacements = 0
    for file in files:
        text = A_GIS.File.read(file=file)
        text, replacements = A_GIS.Text.find_and_replace(
            text=text, old=old, new=new, is_regex=is_regex
        )
        total_replacements += replacements
        A_GIS.File.write(content=text, file=file)

    # Return text
    return total_replacements
