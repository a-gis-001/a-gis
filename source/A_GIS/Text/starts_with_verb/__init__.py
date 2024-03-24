def starts_with_verb(*, sentence: str, do_second_pass: bool = True):
    """Check a sentence starts with a verb

    Uses natural language processing.

    """
    import nltk
    import A_GIS.Text.get_root_word

    nltk.download("averaged_perceptron_tagger")

    # Tokenize into words.
    words = nltk.word_tokenize(sentence)
    if not words:
        return False

    # Get part of speech tags.
    pos_tags = nltk.pos_tag(words)

    # Simple return if starts with verb.
    if pos_tags[0][1] == "VB":
        return True

    if do_second_pass:
        words = ["Do", words[0].lower(), *words[1:]]
        pos_tags = nltk.pos_tag(words)
        if pos_tags[1][1] == "VB":
            return True

    # If we get here, it was not a verb.
    return False
