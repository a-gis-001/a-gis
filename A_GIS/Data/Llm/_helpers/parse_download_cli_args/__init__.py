def parse_download_cli_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("MODEL", type=str, default=None, nargs="?")
    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="Name of the Git branch to download from.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="Number of files to download simultaneously.",
    )
    parser.add_argument(
        "--text-only", action="store_true", help="Only download text files (txt/json)."
    )
    parser.add_argument(
        "--specific-file",
        type=str,
        default=None,
        help="Name of the specific file to download (if not provided, downloads all).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="The folder where the model should be saved.",
    )
    parser.add_argument(
        "--clean", action="store_true", help="Does not resume the previous download."
    )
    parser.add_argument(
        "--check", action="store_true", help="Validates the checksums of model files."
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Max retries count when get error in download time.",
    )
    return parser.parse_args()
