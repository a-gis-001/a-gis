def download(
    *,
    model,
    branch="main",
    threads=4,
    text_only=False,
    specific_file=None,
    output=None,
    clean=False,
    check=True,
    max_retries=5,
):
    """
    Downloads models from Hugging Face to models/username_modelname.

    Example:
    python download-model.py facebook/opt-1.3b

    """

    import base64
    import json
    import os
    import re
    import sys
    from pathlib import Path
    import hashlib
    import requests
    import tqdm
    from requests.adapters import HTTPAdapter

    base = "https://huggingface.co"

    class _ModelDownloader:
        def __init__(self, max_retries=5):
            self.session = requests.Session()
            if max_retries:
                self.session.mount(
                    "https://cdn-lfs.huggingface.co",
                    HTTPAdapter(max_retries=max_retries),
                )
                self.session.mount(
                    "https://huggingface.co", HTTPAdapter(max_retries=max_retries)
                )
            if os.getenv("HF_USER") is not None and os.getenv("HF_PASS") is not None:
                self.session.auth = (os.getenv("HF_USER"), os.getenv("HF_PASS"))
            if os.getenv("HF_TOKEN") is not None:
                self.session.headers = {
                    "authorization": f'Bearer {os.getenv("HF_TOKEN")}'
                }

        def check_model_files(self, model, branch, links, sha256, output_folder):
            # Validate the checksums
            validated = True
            for i in range(len(sha256)):
                fpath = output_folder / sha256[i][0]

                if not fpath.exists():
                    print(f"The following file is missing: {fpath}")
                    validated = False
                    continue

                with open(output_folder / sha256[i][0], "rb") as f:
                    file_hash = hashlib.file_digest(f, "sha256").hexdigest()
                    if file_hash != sha256[i][1]:
                        print(f"Checksum failed: {sha256[i][0]}  {sha256[i][1]}")
                        validated = False
                    else:
                        print(f"Checksum validated: {sha256[i][0]}  {sha256[i][1]}")

            if validated:
                print("[+] Validated checksums of all model files!")
            else:
                print(
                    "[-] Invalid checksums. Rerun download-model.py with the --clean flag."
                )

    if model is None:
        print(
            "Error: Please specify the model you'd like to download (e.g. 'download(model='facebook/opt-1.3b')."
        )
        sys.exit()

    downloader = _ModelDownloader(max_retries=max_retries)

    # Clean up the model/branch names
    import A_GIS.Data.Llm._helpers

    model, branch = A_GIS.Data.Llm._helpers.sanitize_model_and_branch_names(
        model, branch
    )

    # Get the download links from Hugging Face
    (
        links,
        sha256,
        is_lora,
        is_llamacpp,
    ) = A_GIS.Data.Llm._helpers.get_download_links(
        downloader.session,
        model,
        branch,
        text_only=text_only,
        specific_file=specific_file,
    )

    # Get the output folder
    output_folder = A_GIS.Data.Llm._helpers.get_output_folder(
        model, branch, is_lora, is_llamacpp=is_llamacpp, base_folder=output
    )

    if check:
        # Check previously downloaded files
        downloader.check_model_files(model, branch, links, sha256, output_folder)
    else:
        # Download files
        A_GIS.Data.Llm._helpers.download_model_files(
            downloader.session,
            model,
            branch,
            links,
            sha256,
            output_folder,
            specific_file=specific_file,
            threads=threads,
            is_llamacpp=is_llamacpp,
        )

    return output_folder


if __name__ == "__main__":
    import A_GIS.Data.Llm._helpers.parse_download_cli_args

    args = A_GIS.Data.Llm._helpers.parse_download_cli_args()

    download(
        model=args.MODEL,
        branch=args.branch,
        threads=args.threads,
        text_only=args.text_only,
        specific_file=args.specific_file,
        output=args.output,
        clean=args.clean,
        check=args.check,
        max_retries=args.max_retries,
    )
