def starts_with_verb(*, sentence: str, do_second_pass: bool = True):
    """Check a sentence starts with a verb

    Uses natural language processing.

    """
    import nltk
    import A_GIS.Text.get_root_word
    import A_GIS.Code.make_struct

    # Check if averaged_perceptron_tagger is downloaded
    try:
        nltk.data.find("taggers/averaged_perceptron_tagger.zip")
    except LookupError:
        nltk.download("averaged_perceptron_tagger")

    # Starts as false.
    result = False
    pos_tags = None
    pos_tags2 = None

    # Tokenize into words.
    words = nltk.word_tokenize(sentence)

    if words:

        # Get part of speech tags.
        pos_tags = nltk.pos_tag(words)

        # Simple return if starts with verb.
        if pos_tags[0][1] == "VB":
            result = True
        elif pos_tags[0][1] not in ["PRP"] and do_second_pass:
            words = ["Do", words[0].lower(), *words[1:]]
            pos_tags2 = nltk.pos_tag(words)
            if pos_tags2[1][1] == "VB":
                result = True

    return A_GIS.Code.make_struct(
        result=result, pos_tags=pos_tags, pos_tags2=pos_tags2
    )
