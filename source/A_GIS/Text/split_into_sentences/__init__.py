def split_into_sentences(*, text):
    """Split text into sentences using spaCy.

    Args:
        text (str): The text to split into sentences.

    Returns:
        list: A list of sentences.

    Raises:
        ImportError:
            If `spacy` is not installed, this function will raise an ImportError.
        SpacyError:
            If there are issues loading the `en_core_web_sm` model, a SpacyError
            will be raised.

    Examples:
        >>> split_into_sentences(text="This is a test. This is merely a test.")
        ['This is a test.', 'This is merely a test.']
    """
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [str(sent) for sent in doc.sents]
