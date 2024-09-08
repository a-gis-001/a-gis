def read_to_text(*, file: type["pathlib.Path"]):
    """Convert files to plain text based on file extension.

    This function reads a file provided by the `pathlib.Path` class and converts its content
    to a string representation, depending on the file's extension. It currently supports
    PDF and DOCX files through internal helper functions and falls back to a general file reading
    method for other file types. Future versions may extend support to additional file types.

    Args:
        file (pathlib.Path):
            The path to the file that needs to be read and converted to text.

    Returns:
        str:
            The content of the file in plain text format.

    Raises:
        None
    """

    if file.suffix == ".pdf":
        import A_GIS.File._read_to_text_pdf

        return A_GIS.File._read_to_text_pdf(file=file)
    elif file.suffix == ".docx":
        import A_GIS.File._read_to_text_docx

        return A_GIS.File._read_to_text_docx(file=file)
    else:
        import A_GIS.File.read

        return A_GIS.File.read(file=file)
