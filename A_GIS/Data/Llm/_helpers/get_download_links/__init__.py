import requests


def get_download_links(
    session: requests.Session,
    model: str,
    branch: str,
    text_only: bool = False,
    specific_file: str = None,
) -> (list, list, bool, bool):
    """
    Gets download links for the specified model and branch from Hugging Face.

    Args:
        session (requests.Session): The session object to handle HTTP requests.
        model (str): The model name.
        branch (str): The branch name.
        text_only (bool, optional): If True, only text files will be downloaded. Defaults to False.
        specific_file (str, optional): Specific file to download. Defaults to None.

    Returns:
        tuple: A tuple containing the list of download links, sha256 checksums,
               a boolean indicating if it's a LORA model, and a boolean for the LLAMAcpp type.
    """
    import json
    import re
    import base64

    base_url = "https://huggingface.co"
    page = f"/api/models/{model}/tree/{branch}"
    cursor = b""

    links = []
    sha256 = []
    classifications = []
    has_pytorch = False
    has_pt = False
    has_gguf = False
    has_safetensors = False
    is_lora = False

    while True:
        url = f"{base_url}{page}" + (f"?cursor={cursor.decode()}" if cursor else "")
        response = session.get(url, timeout=10)
        response.raise_for_status()
        content = response.content

        data = json.loads(content)
        if len(data) == 0:
            break

        for item in data:
            fname = item["path"]
            if specific_file not in [None, ""] and fname != specific_file:
                continue

            if not is_lora and fname.endswith(
                ("adapter_config.json", "adapter_model.bin")
            ):
                is_lora = True

            is_pytorch = re.match(r"(pytorch|adapter|gptq)_model.*\.bin", fname)
            is_safetensors = re.match(r".*\.safetensors", fname)
            is_pt = re.match(r".*\.pt", fname)
            is_gguf = re.match(r".*\.gguf", fname)
            is_tiktoken = re.match(r".*\.tiktoken", fname)
            is_tokenizer = (
                re.match(r"(tokenizer|ice|spiece).*\.model", fname) or is_tiktoken
            )
            is_text = re.match(r".*\.(txt|json|py|md)", fname) or is_tokenizer

            if any((is_pytorch, is_safetensors, is_pt, is_gguf, is_tokenizer, is_text)):
                if "lfs" in item:
                    sha256.append([fname, item["lfs"]["oid"]])

                if is_text:
                    links.append(
                        f"https://huggingface.co/{model}/resolve/{branch}/{fname}"
                    )
                    classifications.append("text")
                    continue

                if not text_only:
                    links.append(
                        f"https://huggingface.co/{model}/resolve/{branch}/{fname}"
                    )
                    if is_safetensors:
                        has_safetensors = True
                        classifications.append("safetensors")
                    elif is_pytorch:
                        has_pytorch = True
                        classifications.append("pytorch")
                    elif is_pt:
                        has_pt = True
                        classifications.append("pt")
                    elif is_gguf:
                        has_gguf = True
                        classifications.append("gguf")

        cursor = (
            base64.b64encode(f'{{"file_name":"{data[-1]["path"]}"}}'.encode()) + b":50"
        )
        cursor = base64.b64encode(cursor)
        cursor = cursor.replace(b"=", b"%3D")

    def remove_pytorch_pt_links(links, classifications):
        new_links = []
        new_classifications = []
        for link, classification in zip(links, classifications):
            if classification not in ["pytorch", "pt"]:
                new_links.append(link)
                new_classifications.append(classification)
        return new_links, new_classifications

    def process_gguf_links(links, classifications, specific_file):
        if specific_file is None:
            has_q4km = any("q4_k_m" in link.lower() for link in links)
            if has_q4km:
                return [link for link in links if "q4_k_m" in link.lower()], [
                    "gguf" for link in links if "q4_k_m" in link.lower()
                ]
            else:
                return [link for link in links if not link.lower().endswith(".gguf")], [
                    classification
                    for link, classification in zip(links, classifications)
                    if not link.lower().endswith(".gguf")
                ]
        return links, classifications

    # Additional processing based on file types
    if (has_pytorch or has_pt) and has_safetensors:
        links, classifications = remove_pytorch_pt_links(links, classifications)

    if has_gguf:
        links, classifications = process_gguf_links(
            links, classifications, specific_file
        )

    is_llamacpp = has_gguf and specific_file is not None
    return links, sha256, is_lora, is_llamacpp
