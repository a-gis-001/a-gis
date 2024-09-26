import argparse
import pathlib
import A_GIS.File.Node.generate_purpose

parser = argparse.ArgumentParser(description="Generate a purpose of a directory.")
parser.add_argument("path", type=str, help="Path to the directory or file.")

args = parser.parse_args()

# Determine the directory to display
input_path = pathlib.Path(args.path)
if input_path.is_file():
    current_dir = input_path.parent
else:
    current_dir = input_path

purpose = A_GIS.File.Node.generate_purpose(directory=current_dir, overwrite_existing=True)

print(f"Purpose written to {current_dir}/_leaf.node.md\n")
print(purpose)
