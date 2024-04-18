def init(*, model="clip-ViT-B-32"):
    """Initialize a model for calculating image vector embeddings.

    Future versions may return an `_Encoder` adapter class that provides a method `encode`
    and may offer additional functionality or options compared to the current approach.

    Args:
        model (str, optional):
            The identifier of the pre-trained model to use for encoding images.
            Defaults to "clip-ViT-B-32". Users can obtain a list of supported models by
            calling `sentence_transformers.util.load_model_list()`.

    Returns:
        sentence_transformers.SentenceTransformer:
            A pre-trained model from the
            sentence transformers library, ready to encode sentences and potentially images
            into vector representations.

    Raises:
        ValueError:
            If the specified model is not available in the sentence transformer's
            pre-trained models list or if the `model` argument is not a string.
    """

    import sentence_transformers

    encoder = sentence_transformers.SentenceTransformer(model)
    return encoder
