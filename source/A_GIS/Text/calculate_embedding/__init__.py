def calculate_embedding(
    *, lines: list, nchunks: int, model="nomic-embed-text"
):
    """Calculate text embeddings for a list of lines in chunks.

    This function processes a list of text lines and calculates their embeddings using an OLLama model, handling the input text in chunks to manage memory usage effectively. It returns the progress of chunk processing, the calculated embeddings, and the original chunks of text.

    Args:
        lines (list(str)): A list of strings representing individual lines of text.
        nchunks (int): The number of chunks to split the text into for embedding calculation.

    Returns:
        tuple(float, numpy.ndarray, list(str)): A tuple containing:
            1. A list of floats representing the progress through each chunk.
            2. A NumPy array containing the embeddings calculated for each chunk.
            3. A list of strings with the original text lines, split into chunks.

    Raises:
        None

    The function uses an OLLama model to generate embeddings for each chunk of text. The size of each chunk is determined by dividing the total number of lines by `nchunks`. The last chunk includes all remaining lines. The progress is tracked as a fraction of completed chunks, and the final entry is set to 1.0 to represent full completion. The embeddings are returned as a NumPy array for efficient numerical computation.
    """

    import numpy as np
    import ollama

    # Concatenate all content and split by lines
    total_lines = len(lines)
    if nchunks > total_lines:
        nchunks = total_lines

    accumulated_lines = 0
    chunks = []
    progress = []
    embeddings = []

    # Calculate chunk size based on the number of chunks
    chunk_size = total_lines // nchunks

    for i in range(nchunks):
        # Handle the last chunk to ensure it includes all remaining lines
        if i == nchunks - 1:
            chunk_lines = lines[accumulated_lines:]
        else:
            chunk_lines = lines[
                accumulated_lines : accumulated_lines + chunk_size
            ]

        chunk_content = "\n".join(chunk_lines)
        chunks.append(chunk_content)

        accumulated_lines += len(chunk_lines)
        progress.append(accumulated_lines / total_lines)

        # Generate the embedding for the current chunk
        # nomic-embed-text,bge-m3,mxbai-embed-large
        embedding_result = ollama.embeddings(
            model=model,
            prompt=f"Calculate an embedding for detecting text similarity:\n{chunk_content}",
        )
        embeddings.append(embedding_result["embedding"])

    # Ensure the final progress value is 1
    if progress[-1] < 1.0:
        progress[-1] = 1.0

    # Convert embeddings to a NumPy array
    embeddings = np.array(embeddings)

    return progress, embeddings, chunks
