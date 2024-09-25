def starts_with_verb(*, sentence: str, do_second_pass: bool = True):
    """Determine if a sentence starts with a verb.

    This function checks whether the first word or a rephrased version
    of it in a given sentence is a verb by using the Natural Language
    Toolkit (nltk) to tokenize the sentence and tag each token with its
    part of speech (POS). It supports an optional second pass where it
    attempts to transform the sentence structurally to better identify a
    verb if the first word is not a verb or a pronoun.

    Args:
        sentence (str):
            The sentence to be analyzed for the presence of a verb at
            the beginning.
        do_second_pass (bool, optional):
            A flag indicating whether a second pass analysis should be
            performed on the sentence. This second pass involves
            rephrasing the first part of the sentence and checking again
            for a verb. The default is True.

    Returns:
        dataclass:
            With the following attributes

            - result (bool): A boolean indicating whether the first
              word or its rephrased version is a verb.
            - pos_tags (list of tuples): A list of tuples containing
              each token and its corresponding POS tag from the first
              pass analysis.
            - pos_tags2 (list of tuples, optional): A list of tuples
              containing each token and its corresponding POS tag from
              the second pass analysis if `do_second_pass` is True.
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
