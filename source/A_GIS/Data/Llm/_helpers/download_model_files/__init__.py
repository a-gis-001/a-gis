def download_model_files(
    session,
    model,
    branch,
    links,
    sha256,
    output_folder,
    progress_bar=None,
    start_from_scratch=False,
    threads=4,
    specific_file=None,
    is_llamacpp=False,
):
    import A_GIS.Data.Llm._helpers.start_download_threads
    import datetime
    import hashlib

    # Create the folder and writing the metadata
    output_folder.mkdir(parents=True, exist_ok=True)

    if not is_llamacpp:
        metadata = (
            f"url: https://huggingface.co/{model}\n"
            f"branch: {branch}\n"
            f'download date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        )

        sha256_str = "\n".join([f"    {item[1]} {item[0]}" for item in sha256])
        if sha256_str:
            metadata += f"sha256sum:\n{sha256_str}"

        metadata += "\n"
        (output_folder / "huggingface-metadata.txt").write_text(metadata)

    if specific_file:
        print(f"Downloading {specific_file} to {output_folder}")
    else:
        print(f"Downloading the model to {output_folder}")

    A_GIS.Data.Llm._helpers.start_download_threads(
        session,
        links,
        output_folder,
        start_from_scratch=start_from_scratch,
        threads=threads,
    )
