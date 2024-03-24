def get_word_stem(*, word: str):
    """Get the stem of a word using natural language processing

    The stem is helpful for categorizing a word.

    - running -> run
    - inserts -> insert

    """
    import nltk
    import nltk.stem.porter

    # Initialize the PorterStemmer
    stemmer = nltk.stem.porter.PorterStemmer()

    return stemmer.stem(word)
