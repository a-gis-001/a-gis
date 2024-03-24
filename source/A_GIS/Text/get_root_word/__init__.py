def get_root_word(*, word: str):
    """Generate word's root form using NLP and Spacy lemmatization.

    This function uses NLP to find the root form of an input word, which
    is useful for categorizing words based on their meanings. For
    instance, 'running' would be reduced to 'run', and 'inserts' would
    become 'insert'. It also requires the `spacy` library and a language
    model like 'en_core_web_sm'. If these are not installed or if the
    provided word is not recognized by the language model, an error may
    occur.

    Args:
        word (str): The word from which to generate the stem.

    Raises:
        None

    Returns:
        str: The root form of the input word, as determined by NLP.

    """

    import spacy

    nlp = spacy.load("en_core_web_sm")
    lemmatizer = nlp.get_pipe("lemmatizer")

    tokens = [token.lemma_ for token in nlp(word)]
    return tokens[0]
