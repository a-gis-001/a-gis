def _read_to_text_docx(*, file: type["pathlib.Path"]):
    """Reads a DOCX and returns text

    Helper function for read_to_text not meant to be used
    directly.
    """
    import docx

    doc = docx.Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text
