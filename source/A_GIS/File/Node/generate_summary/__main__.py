import argparse
import pathlib
import A_GIS.File.Node.generate_summary

parser = argparse.ArgumentParser(description="Generate a summary of a directory.")
parser.add_argument("path", type=str, help="Path to the directory or file.")

args = parser.parse_args()

# Determine the directory to display
input_path = pathlib.Path(args.path)
if input_path.is_file():
    current_dir = input_path.parent
else:
    current_dir = input_path

print(A_GIS.File.Node.generate_summary(directory=current_dir))
