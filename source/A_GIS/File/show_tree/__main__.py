import argparse
import pathlib
import A_GIS.File.show_tree

parser = argparse.ArgumentParser(description="Display a directory tree.")
parser.add_argument("path", type=str, help="Path to the directory or file.")
parser.add_argument("--max_levels", type=int, default=3, help="Maximum levels to display in the tree.")
parser.add_argument("--num_per_dir", type=int, default=10, help="Number of entries to show per directory.")
parser.add_argument("--root", type=str, default=None, help="root directory.")
parser.add_argument("--extensions", nargs='*', default=None, help="List of file extensions to include.")

args = parser.parse_args()

# Determine the directory to display
input_path = pathlib.Path(args.path)
if input_path.is_file():
    current_dir = input_path.parent
else:
    current_dir = input_path

print(
    A_GIS.File.show_tree(
        directory=current_dir,
        max_levels=args.max_levels,
        num_per_dir=args.num_per_dir,
        only_extensions=args.extensions,
        root_dir=args.root
    )
)
