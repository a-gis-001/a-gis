import requests
from pathlib import Path


def download(
    session: requests.Session,
    url: str,
    output_folder: Path,
    start_from_scratch: bool = False,
):
    """
    Downloads a single file from a given URL.

    Args:
        session (requests.Session): The session object to handle HTTP requests.
        url (str): The URL from which to download the file.
        output_folder (Path): The folder where the file will be saved.
        start_from_scratch (bool, optional): If True, any existing file will be overwritten. Defaults to False.
    """
    import tqdm
    import os

    filename = Path(url.rsplit("/", 1)[1])
    output_path = output_folder / filename
    headers = {}
    mode = "wb"

    if output_path.exists() and not start_from_scratch:
        # Resume the download from where it left off
        r = session.get(url, stream=True, timeout=10)
        total_size = int(r.headers.get("content-length", 0))
        if output_path.stat().st_size >= total_size:
            return

        headers = {"Range": f"bytes={output_path.stat().st_size}-"}
        mode = "ab"

    with session.get(url, stream=True, headers=headers, timeout=10) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        block_size = 1024 * 1024  # 1MB

        tqdm_kwargs = {
            "total": total_size,
            "unit": "iB",
            "unit_scale": True,
            "bar_format": "{l_bar}{bar}| {n_fmt:6}/{total_fmt:6} {rate_fmt:6}",
        }

        if "COLAB_GPU" in os.environ:
            tqdm_kwargs.update({"position": 0, "leave": True})

        with open(output_path, mode) as f:
            with tqdm.tqdm(**tqdm_kwargs) as t:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
