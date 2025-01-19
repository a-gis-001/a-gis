import argparse
import pathlib
import A_GIS.File.Node.generate_purpose

# Create the argument parser
parser = argparse.ArgumentParser(description="Generate a purpose for a directory.")
parser.add_argument("path", type=str, help="Path to the directory or file.")
parser.add_argument("--overwrite", action="store_true", help="Overwrite the existing file if it exists.")

# Parse the arguments
args = parser.parse_args()

# Determine the directory to process
input_path = pathlib.Path(args.path)
if input_path.is_file():
    current_dir = input_path.parent
else:
    current_dir = input_path

# Generate the purpose
purpose = A_GIS.File.Node.generate_purpose(directory=current_dir, overwrite_existing=args.overwrite)

# Print the output or write to the file
if args.overwrite:
    print(f"Purpose written to {current_dir}/_leaf.node.md\n")
print(purpose)
