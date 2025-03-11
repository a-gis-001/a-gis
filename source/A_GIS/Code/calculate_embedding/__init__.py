def calculate_embedding(
    *,
    code: str,
    reference: str = "def do_thing():\n    pass",
    compare: list[str] = [],
    model: str = "microsoft/graphcodebert-base",
    instruction: str = "Represent this Python code for semantic/logical similarity",
    transformers_warnings=False,
):
    """Calculate embeddings using GraphCodeBERT, CodeT5+, or Instructor-XL."""
    import transformers
    import numpy as np
    import torch
    import A_GIS.Code.make_struct
    import logging

    # Suppress warning messages from Hugging Face transformers
    if not transformers_warnings:
        logging.getLogger("transformers").setLevel(logging.ERROR)

    def cos_sim(a, b):
        return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

    # Function to orthogonalize a vector with respect to reference
    def orthogonalize(v, ref):
        # Project v onto ref
        proj = np.dot(v, ref) / np.dot(ref, ref) * ref
        # Subtract projection to get orthogonal component
        return v - proj

    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

    # Load tokenizer and model
    tokenizer = transformers.AutoTokenizer.from_pretrained(model, trust_remote_code=True)

    # Fix for StarCoder (models without a pad token)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Ensure model_max_length is a reasonable value
    max_length = min(tokenizer.model_max_length, 8192)  # Cap at 8192 tokens max

    embedder = transformers.AutoModel.from_pretrained(model, trust_remote_code=True).to(device)

    def get_embedding(text):
        if "instructor" in model.lower():
            text = f"{instruction}: {text}"  # Instructor-XL requires an instruction

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            if "instructor" in model.lower():
                # Instructor-XL (T5-based model) requires decoder_input_ids
                outputs = embedder(**inputs, decoder_input_ids=torch.zeros((1, 1), dtype=torch.long, device=device))
                return outputs.encoder_last_hidden_state[:, 0, :].detach().cpu().numpy()

            else:
                # GraphCodeBERT and CodeT5+
                outputs = embedder(**inputs)
                if isinstance(outputs, torch.Tensor):  # CodeT5+
                    return outputs.detach().cpu().numpy()
                elif hasattr(outputs, "last_hidden_state"):  # GraphCodeBERT
                    return outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
                else:
                    raise ValueError("Unsupported model output format.")

    # Gather all text blocks
    blocks = [reference, code] + compare
    embeddings = np.vstack([get_embedding(block) for block in blocks])
    token_counts = [len(tokenizer.encode(block, truncation=False)) for block in blocks]


    # Compute embeddings relative to reference
    reference_embedding = embeddings[0]
    reference_tokens = token_counts[0]
    code_embedding = orthogonalize(embeddings[1],reference_embedding)
    code_tokens = token_counts[1]
    if len(embeddings)>2:
        compare_embeddings = orthogonalize(embeddings[2:], reference_embedding)
        compare_tokens = token_counts[2:]
    else:
        compare_embeddings=[]
        compare_tokens=[]

    # Compute similarity scores
    similarity = [float(cos_sim(code_embedding, c)) for c in compare_embeddings]

    return A_GIS.Code.make_struct(
        _code=code,
        _compare=compare,
        _reference=reference,
        reference_embedding=reference_embedding,
        code_embedding=code_embedding,
        compare_embeddings=compare_embeddings,
        similarity=similarity,
        reference_tokens=reference_tokens,
        code_tokens=code_tokens,
        compare_tokens=compare_tokens,
        max_token_length=max_length
    )
