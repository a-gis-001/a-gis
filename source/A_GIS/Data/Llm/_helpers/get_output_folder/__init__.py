def get_output_folder(
    model: str,
    branch: str,
    is_lora: bool,
    is_llamacpp: bool = False,
    base_folder: str = None,
) -> type["pathlib.Path"]:
    """
    Determines the output folder for the downloaded model.

    Args:
        model (str): The model name.
        branch (str): The branch name.
        is_lora (bool): Indicates if the model is a LORA model.
        is_llamacpp (bool, optional): Indicates if the model is of type GGUF. Defaults to False.
        base_folder (str, optional): Base folder for the model storage. Defaults to None.

    Returns:
        Path: The calculated output folder as a Path object.
    """
    import pathlib.Path

    if base_folder is None:
        base_folder = "models" if not is_lora else "loras"

    if is_llamacpp:
        return pathlib.Path(base_folder)

    output_folder = f"{'_'.join(model.split('/')[-2:])}"
    if branch != "main":
        output_folder += f"_{branch}"

    return pathlib.Path(base_folder) / output_folder
