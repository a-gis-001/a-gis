def split_into_sentences(*, text: str):
    """Extract and returns a list of sentences.

    The spaCy model `en_core_web_sm` is loaded internally to perform the
    sentence segmentation.

    Args:
        text (str):
            The text string that needs to be split into sentences.

    Returns:
        List[str]:
            A list of sentences extracted from the input text.

    Raises:
        ImportError:
            If `spacy` is not installed, this function will raise an ImportError.
        SpacyError:
            If there are issues loading the `en_core_web_sm` model, a SpacyError
            will be raised.

    Examples:
        >>> split_into_sentences("This is a test. This is merely a test.")
        ['This is a test.', 'This is merely a test.']
    """

    import spacy

    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the text using spaCy
    doc = nlp(text)

    # Extract sentences
    sentences = [sent.text for sent in doc.sents]
    return sentences
