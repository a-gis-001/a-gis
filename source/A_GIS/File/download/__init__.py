import requests
import pathlib

def download(
    *,
    url: str,
    output_folder: pathlib.Path,
    filename: pathlib.Path = None,
    session: requests.Session = None,
    start_from_scratch: bool = False,
    leave_progress_bar: bool = True,
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
    import mimetypes

    # Update inputs.
    output_folder = pathlib.Path(output_folder)

    # Get filename or derive from URL
    if filename is None:
        filename = pathlib.Path(url.rsplit("/", 1)[1])
    filename = pathlib.Path(filename)

    if session is None:
        session = requests.Session()

    if not filename.suffix:
        # Get the correct extension if it's missing
        try:
            get_resp = session.get(url, stream=True, timeout=10)
            get_resp.raise_for_status()
            content_type = get_resp.headers.get("Content-Type")
            if content_type:
                ext = mimetypes.guess_extension(content_type.split(";")[0])
                if ext:
                    filename = filename.with_suffix(ext)
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to determine file extension. {e}")

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
            "leave": leave_progress_bar,
        }

        if "COLAB_GPU" in os.environ:
            tqdm_kwargs.update({"position": 0})

        with open(output_path, mode) as f:
            with tqdm.tqdm(**tqdm_kwargs) as t:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
