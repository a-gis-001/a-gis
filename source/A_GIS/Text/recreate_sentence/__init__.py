def recreate_sentence(*, tokens: list[str]):
    """Recreate a sentence from tokens"""

    # List of punctuation that should not be preceded by a space
    no_space_before = {".", ",", "!", "?", ":", ";", "'", ")", "]", "}"}
    # List of punctuation that should not be followed by a space
    no_space_after = {"(", "[", "{"}

    sentence = ""
    for i, token in enumerate(tokens):
        if i == 0:
            sentence += token
        elif token in no_space_before:
            sentence += token
        elif i > 0 and tokens[i - 1] in no_space_after:
            sentence += token
        else:
            sentence += " " + token

    # Replace with simple quotes.
    sentence = sentence.replace("``", '"').replace("''", '"')

    return sentence
