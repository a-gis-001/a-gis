import pathlib


def write(*, content, file: pathlib.Path, binary: bool = False):
    mode = "w"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        f.write(content)
