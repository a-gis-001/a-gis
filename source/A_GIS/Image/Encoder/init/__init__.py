def init(*, model="clip-ViT-B-32"):
    """Initialize an encoder for calculating image embeddings.

    Currently this function initializes a sentence transformer model with the given name
    and returns its instance and simply returns it. 
    
    Future versions of this function may return an `_Encoder` adapter class 
    that has a method `encode` and provides different options than transformers.

    Args:
        model (str, optional):
            The identifier of the pre-trained model to use. Defaults to
            "clip-ViT-B-32". Supported models can be listed using `sentence_transformers.util.load_model_list()`.

    Returns:
        SentenceTransformer:
            A pre-trained model from the sentence transformers library,
            ready to encode sentences into vector representations.

    Raises:
        ValueError:
            If the specified model is not available in the sentence transformer's
            pre-trained models list.
    """

    import sentence_transformers

    encoder = sentence_transformers.SentenceTransformer(model)
    return encoder
