def _read_to_text_pdf(*, file: type["pathlib.Path"]) -> str:
    """Reads a PDF and returns text

    Helper function for read_to_text not meant to be used
    directly.
    """
    import PyPDF2

    with open(file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text
