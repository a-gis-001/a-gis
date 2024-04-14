def init(*, model="clip-ViT-B-32"):
    import sentence_transformers

    encoder = sentence_transformers.SentenceTransformer(model)
    return encoder
