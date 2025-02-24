def calculate_embedding(
    *,
    code: str,
    reference: str='def do_thing():\n    pass',
    compare: list[str] = [],
    model: str = "microsoft/graphcodebert-base",
):
    """Calculate embeddings of code."""
    import transformers
    import numpy
    import torch
    import A_GIS.Code.make_struct

    def cos_sim(a, b):
        return (a @ b.T) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))

    # Initialize tokenizer and model
    tokenizer = transformers.AutoTokenizer.from_pretrained(model,trust_remote_code=True)
    embedder = transformers.AutoModel.from_pretrained(model,trust_remote_code=True)

    def get_embedding(text):
        # Tokenize and get model output
        inputs = tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        )
        outputs = embedder(**inputs,return_dict=True)
        # mean-pooling gives less differentiation.
        #return outputs.last_hidden_state.mean(dim=1).detach().numpy()
        # Use [CLS] token embedding as code embedding
        return outputs.last_hidden_state[:, 0, :].detach().numpy()
        # Max pooling across token embeddings (dim=1 means across sequence length)
        #max_pooled = torch.max(outputs.last_hidden_state, dim=1).values
        #return max_pooled.detach().cpu().numpy()  # Ensure it's detached before converting to NumPy

    blocks = []
    blocks.append(reference)
    blocks.append(code)
    blocks.extend(compare)

    embeddings = [get_embedding(block) for block in blocks]
    embeddings = numpy.vstack(embeddings)

    reference_embedding = embeddings[0]
    code_embedding = embeddings[1] - reference_embedding

    similarity = []
    compare_embeddings = []
    for i in range(2, len(embeddings)):
        c = embeddings[i] - reference_embedding
        compare_embeddings.append(c)
        similarity.append(
            float(cos_sim(code_embedding, c))
        )

    return A_GIS.Code.make_struct(
        _code=code,
        _compare=compare,
        _reference=reference,
        reference_embedding=reference_embedding,
        code_embedding=code_embedding,
        compare_embeddings=compare_embeddings,
        similarity=similarity,
    )
