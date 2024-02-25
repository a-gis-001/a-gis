import pathlib


def read(*, file: pathlib.Path, binary: bool = False):
    mode = "r"
    if binary:
        mode += "b"
    with open(file, mode) as f:
        return f.read()
